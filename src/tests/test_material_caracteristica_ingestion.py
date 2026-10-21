"""Trava a carga de característica por codigoItem, pulando itens já gravados."""

from pytest import MonkeyPatch

from etl.ingestion.material.material_caracteristica import (
    caracteristica_item_query_params,
    main,
)


class CapturedBatchRun:
    """Falso que guarda os argumentos da carga por código de item."""

    def __init__(self) -> None:
        self.kwargs: dict[str, object] = {}

    def __call__(self, **kwargs: object) -> int:
        """Registra a chamada e devolve zero linhas gravadas."""
        self.kwargs = kwargs
        return 0


def test_caracteristica_item_query_params_sends_codigo_item() -> None:
    assert caracteristica_item_query_params(206504) == {"codigoItem": 206504}


def test_main_walks_missing_material_item_codes(monkeypatch: MonkeyPatch) -> None:
    captured = CapturedBatchRun()
    monkeypatch.setattr(
        "etl.ingestion.material.material_caracteristica.run_preco_batch_ingestion",
        captured,
    )
    main()
    assert captured.kwargs["catalog_table"] == "material_item"
    assert captured.kwargs["catalog_column"] == "cod_item"
    assert captured.kwargs["absent_dest_table"] == "material_caracteristica"
    assert captured.kwargs["absent_dest_column"] == "cod_item"
    assert captured.kwargs["batch_size"] == 20
    assert captured.kwargs["parallel_codes"] == 4
    assert captured.kwargs["page_size"] == 500
    assert captured.kwargs["endpoint_path"] == (
        "/modulo-material/7_consultarMaterialCaracteristicas"
    )
    assert captured.kwargs["table_name"] == "material_caracteristica"
    assert captured.kwargs["job_name"] == "material_caracteristica_item"
    params = captured.kwargs["params_for_code"]
    assert params(206504) == {"codigoItem": 206504}

import pytest
from pydantic import ValidationError

from contracts.material_caracteristica import MaterialCaracteristicaRecord


def _valid_kwargs() -> dict[str, object]:
    return {
        "cod_item": 9001,
        "item_sustentavel": True,
        "status_item": True,
        "codigo_caracteristica": "c1",
        "nome_caracteristica": "cor",
        "status_caracteristica": True,
        "codigo_valor_caracteristica": "v1",
        "nome_valor_caracteristica": "azul",
        "status_valor_caracteristica": True,
        "numero_caracteristica": 1,
        "sigla_unidade_medida": "un",
        "data_hora_atualizacao": "2022-01-01T00:00:00",
    }


def test_material_caracteristica_uppercases_text_fields() -> None:
    record = MaterialCaracteristicaRecord(**_valid_kwargs())  # type: ignore[arg-type]
    assert record.codigo_caracteristica == "C1"
    assert record.nome_caracteristica == "COR"
    assert record.codigo_valor_caracteristica == "V1"
    assert record.nome_valor_caracteristica == "AZUL"
    assert record.sigla_unidade_medida == "UN"


def test_material_caracteristica_rejects_non_int_cod_item() -> None:
    kwargs = _valid_kwargs()
    kwargs["cod_item"] = "9001"
    with pytest.raises(ValidationError):
        MaterialCaracteristicaRecord(**kwargs)  # type: ignore[arg-type]


def test_material_caracteristica_accepts_null_optional_fields() -> None:
    kwargs = _valid_kwargs()
    kwargs["item_sustentavel"] = None
    kwargs["status_item"] = None
    kwargs["nome_caracteristica"] = None
    kwargs["status_caracteristica"] = None
    kwargs["nome_valor_caracteristica"] = None
    kwargs["status_valor_caracteristica"] = None
    kwargs["sigla_unidade_medida"] = None
    kwargs["data_hora_atualizacao"] = None
    record = MaterialCaracteristicaRecord(**kwargs)  # type: ignore[arg-type]
    assert record.nome_caracteristica is None
    assert record.sigla_unidade_medida is None

import pytest

from etl.ingestion.legado.map_legado_fields import (
    legado_compra_sem_licitacao_fields,
    legado_item_licitacao_fields,
    legado_item_pregao_fields,
    legado_item_sem_licitacao_fields,
    legado_licitacao_fields,
    legado_pregao_fields,
    legado_rdc_fields,
    pick_row_fields,
)


def test_legado_licitacao_fields_maps_identity() -> None:
    fields = legado_licitacao_fields(
        {
            "id_compra": "123",
            "objeto": "notebook",
            "valor_estimado_total": 10,
        }
    )
    assert fields["id_compra"] == "123"
    assert fields["objeto"] == "notebook"
    assert fields["valor_estimado_total"] == 10
    assert fields["uasg"] is None


def test_legado_item_licitacao_fields_maps_ids() -> None:
    fields = legado_item_licitacao_fields(
        {"id_compra": "c1", "id_compra_item": "i1", "nome_uasg": "uasg"}
    )
    assert fields["id_compra_item"] == "i1"
    assert fields["quantidade"] is None


def test_legado_pregao_fields_keeps_api_no_ausg() -> None:
    fields = legado_pregao_fields({"id_compra": "p1", "no_ausg": "centro"})
    assert fields["no_ausg"] == "centro"
    assert fields["valor_estimado_total"] is None


def test_legado_item_pregao_fields_maps_amounts() -> None:
    fields = legado_item_pregao_fields(
        {"id_compra": "p1", "id_compra_item": "i1", "quantidade_item": "3"}
    )
    assert fields["quantidade_item"] == "3"


def test_legado_compra_sem_licitacao_fields_maps_ano() -> None:
    fields = legado_compra_sem_licitacao_fields(
        {"id_compra": "d1", "dt_ano_aviso": 2024}
    )
    assert fields["dt_ano_aviso"] == 2024
    assert fields["ds_objeto_licitacao"] is None


def test_legado_item_sem_licitacao_fields_maps_composite() -> None:
    fields = legado_item_sem_licitacao_fields(
        {"id_compra": "d1", "id_compra_item": "i2", "co_orgao": "36000"}
    )
    assert fields["co_orgao"] == "36000"


def test_pick_row_fields_requires_identity_keys() -> None:
    with pytest.raises(KeyError, match="id_compra"):
        pick_row_fields({"objeto": "x"}, ("id_compra",), ("id_compra", "objeto"))


def test_legado_rdc_fields_maps_identificador() -> None:
    fields = legado_rdc_fields({"identificador": "rdc-1", "uasg": 153001})
    assert fields["identificador"] == "rdc-1"
    assert fields["uasg"] == 153001
    assert fields["objeto"] is None

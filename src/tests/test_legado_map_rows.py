from etl.ingestion.legado.legado_compra_sem_licitacao import (
    map_legado_compra_sem_licitacao_row,
)
from etl.ingestion.legado.legado_item_licitacao import map_legado_item_licitacao_row
from etl.ingestion.legado.legado_item_pregao import map_legado_item_pregao_row
from etl.ingestion.legado.legado_item_sem_licitacao import (
    map_legado_item_sem_licitacao_row,
)
from etl.ingestion.legado.legado_licitacao import map_legado_licitacao_row
from etl.ingestion.legado.legado_pregao import map_legado_pregao_row
from etl.ingestion.legado.legado_rdc import map_legado_rdc_row


def test_map_legado_licitacao_row() -> None:
    record = map_legado_licitacao_row(
        {
            "id_compra": "123",
            "uasg": 153001,
            "modalidade": 5,
            "nome_modalidade": "pregao",
            "objeto": "notebook",
            "pertence14133": False,
        }
    )
    assert record.id_compra == "123"
    assert record.uasg == 153001
    assert record.nome_modalidade == "PREGAO"


def test_map_legado_item_licitacao_row() -> None:
    record = map_legado_item_licitacao_row(
        {
            "id_compra": "c1",
            "id_compra_item": "i1",
            "uasg": 153001,
            "nome_material": "cadeira",
        }
    )
    assert record.id_compra_item == "i1"
    assert record.nome_material == "CADEIRA"


def test_map_legado_pregao_row() -> None:
    record = map_legado_pregao_row(
        {"id_compra": "p1", "no_ausg": "centro", "valor_estimado_total": "9.5"}
    )
    assert record.no_ausg == "CENTRO"
    assert record.valor_estimado_total == 9.5


def test_map_legado_item_pregao_row() -> None:
    record = map_legado_item_pregao_row(
        {"id_compra": "p1", "id_compra_item": "i1", "descricao_item": "item"}
    )
    assert record.descricao_item == "ITEM"


def test_map_legado_compra_sem_licitacao_row() -> None:
    record = map_legado_compra_sem_licitacao_row(
        {"id_compra": "d1", "ds_objeto_licitacao": "servico", "dt_ano_aviso": 2024}
    )
    assert record.dt_ano_aviso == 2024


def test_map_legado_item_sem_licitacao_row() -> None:
    record = map_legado_item_sem_licitacao_row(
        {"id_compra": "d1", "id_compra_item": "i2", "no_servico": "limpeza"}
    )
    assert record.no_servico == "LIMPEZA"


def test_map_legado_rdc_row() -> None:
    record = map_legado_rdc_row(
        {"identificador": "rdc-1", "objeto": "obra", "uf_uasg": "sp"}
    )
    assert record.identificador == "rdc-1"
    assert record.uf_uasg == "SP"

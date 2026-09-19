import pytest

from etl.ingestion.planejamento.pgc_agregacao import map_pgc_agregacao_row
from etl.ingestion.planejamento.pgc_detalhe import map_pgc_detalhe_row
from etl.ingestion.planejamento.pgc_detalhe_catalogo import map_pgc_detalhe_catalogo_row


def test_map_pgc_detalhe_row() -> None:
    record = map_pgc_detalhe_row(
        {
            "codigoUasg": "153001",
            "nomeUasg": "uasg centro",
            "orgao": "36000",
            "numeroArtefato": 12,
            "anoArtefato": 2026,
            "ordemDfd": 1,
            "codigoItemCatalogo": 449156,
            "descricaoItemCatalogo": "notebook",
            "anoPcaProjetoCompra": 2026,
            "quantidadeItem": 2,
            "valorUnitarioItem": 10,
        }
    )
    assert record.codigo_uasg == "153001"
    assert record.descricao_item_catalogo == "NOTEBOOK"
    assert record.codigo_item_catalogo == "449156"
    assert record.quantidade_item == 2.0


def test_map_pgc_detalhe_row_requires_orgao() -> None:
    with pytest.raises(KeyError, match="orgao"):
        map_pgc_detalhe_row(
            {
                "codigoUasg": "153001",
                "numeroArtefato": 1,
                "anoArtefato": 2026,
                "ordemDfd": 0,
                "codigoItemCatalogo": "1",
                "anoPcaProjetoCompra": 2026,
            }
        )


def test_map_pgc_detalhe_catalogo_row_shares_detalhe_shape() -> None:
    record = map_pgc_detalhe_catalogo_row(
        {
            "codigoUasg": "1",
            "orgao": "36000",
            "numeroArtefato": 2,
            "anoArtefato": 2026,
            "ordemDfd": 0,
            "codigoItemCatalogo": "9",
            "anoPcaProjetoCompra": 2026,
            "tipoItem": "Material",
        }
    )
    assert record.tipo_item == "MATERIAL"


def test_map_pgc_agregacao_row() -> None:
    record = map_pgc_agregacao_row(
        {
            "orgao": "36000",
            "ano": 2026,
            "poder": "executivo",
            "esfera": "federal",
            "quantidadeTotalItens": 3,
            "valorTotalEstimado": 10,
        }
    )
    assert record.poder == "EXECUTIVO"
    assert record.quantidade_total_itens == 3
    assert record.valor_total_estimado == 10.0

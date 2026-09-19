import pytest

from etl.ingestion.precos.preco_material import map_preco_material_row
from etl.ingestion.precos.preco_material_detalhe import map_preco_material_detalhe_row
from etl.ingestion.precos.preco_servico import map_preco_servico_row
from etl.ingestion.precos.preco_servico_detalhe import map_preco_servico_detalhe_row


def test_map_preco_material_row() -> None:
    record = map_preco_material_row(
        {
            "idCompra": 10,
            "idItemCompra": 2,
            "numeroItemCompra": 1,
            "codigoItemCatalogo": 123,
            "descricaoItem": "notebook",
            "precoUnitario": 99.9,
            "quantidade": 3,
            "nomeFornecedor": "acme",
            "marca": "dell",
            "codigoPdm": "1001",
            "nomePdm": "pdm",
            "codigoClasse": 101,
            "nomeClasse": "classe",
            "idCompraItem": "item-1",
            "siglaUnidadeFornecimento": "un",
            "nomeUnidadeFornecimento": "unidade",
            "capacidadeUnidadeFornecimento": 1,
        }
    )
    assert record.id_compra == "10"
    assert record.codigo_item_catalogo == 123
    assert record.descricao_item == "NOTEBOOK"
    assert record.marca == "DELL"
    assert record.preco_unitario == 99.9
    assert record.codigo_pdm == "1001"


def test_map_preco_material_detalhe_row() -> None:
    record = map_preco_material_detalhe_row(
        {
            "idCompra": "c-1",
            "idItemCompra": 2,
            "numeroItemCompra": 3,
            "codigoItemCatalogo": 123,
            "objetoCompra": "compra",
            "descricaoDetalhadaItem": "detalhe",
            "dataAtualizacaoFato": "2024-01-15T10:30:00",
        }
    )
    assert record.id_compra == "c-1"
    assert record.objeto_compra == "COMPRA"
    assert record.numero_item_compra == 3


def test_map_preco_servico_row() -> None:
    record = map_preco_servico_row(
        {
            "idCompra": "s-9",
            "idItemCompra": 8,
            "codigoItemCatalogo": 7250,
            "descricaoItem": "limpeza",
            "precoUnitario": 1.25,
            "nomeUnidadeMedida": "hora",
            "siglaUnidadeMedida": "h",
        }
    )
    assert record.id_compra == "s-9"
    assert record.descricao_item == "LIMPEZA"
    assert record.sigla_unidade_medida == "H"


def test_map_preco_material_row_requires_id_compra() -> None:
    with pytest.raises(KeyError, match="idCompra"):
        map_preco_material_row({"idItemCompra": 1, "codigoItemCatalogo": 123})


def test_map_preco_servico_detalhe_row() -> None:
    record = map_preco_servico_detalhe_row(
        {
            "idCompra": 44,
            "idItemCompra": 5,
            "codigoItemCatalogo": 7250,
            "objetoCompra": "servico",
            "descricaoDetalhadaItem": "escopo",
            "dataAtualizacaoFato": "2024-01-15T10:30:00",
        }
    )
    assert record.codigo_item_catalogo == 7250
    assert record.descricao_detalhada_item == "ESCOPO"

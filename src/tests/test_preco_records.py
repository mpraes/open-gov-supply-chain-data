import pytest
from pydantic import ValidationError

from contracts.preco_material import PrecoMaterialRecord
from contracts.preco_material_detalhe import PrecoMaterialDetalheRecord
from contracts.preco_servico import PrecoServicoRecord
from contracts.preco_servico_detalhe import PrecoServicoDetalheRecord


def test_preco_material_coerces_id_and_uppercases_text() -> None:
    record = PrecoMaterialRecord(
        id_compra=99,
        id_item_compra=1,
        codigo_item_catalogo=123,
        descricao_item=" notebook ",
        nome_fornecedor=" fornecedor x ",
        preco_unitario=10,
        quantidade=2,
    )
    assert record.id_compra == "99"
    assert record.descricao_item == "NOTEBOOK"
    assert record.nome_fornecedor == "FORNECEDOR X"
    assert record.preco_unitario == 10.0
    assert record.quantidade == 2.0


def test_preco_material_rejects_string_preco() -> None:
    with pytest.raises(ValidationError):
        PrecoMaterialRecord(
            id_compra="1",
            id_item_compra=1,
            codigo_item_catalogo=123,
            preco_unitario="10.0",  # type: ignore[arg-type]
        )


def test_preco_material_detalhe_uppercases_objeto() -> None:
    record = PrecoMaterialDetalheRecord(
        id_compra="c1",
        id_item_compra=2,
        codigo_item_catalogo=123,
        objeto_compra=" aquisicao ",
        descricao_detalhada_item=" item detalhe ",
        data_atualizacao_fato="2024-01-15T10:30:00",
    )
    assert record.objeto_compra == "AQUISICAO"
    assert record.descricao_detalhada_item == "ITEM DETALHE"


def test_preco_servico_coerces_id_compra_and_price() -> None:
    record = PrecoServicoRecord(
        id_compra="compra-1",
        id_item_compra=8,
        codigo_item_catalogo=7250,
        descricao_item=" limpeza ",
        preco_unitario=1.25,
    )
    assert record.id_compra == "compra-1"
    assert record.descricao_item == "LIMPEZA"
    assert record.preco_unitario == 1.25


def test_preco_servico_detalhe_requires_ids() -> None:
    with pytest.raises(ValidationError):
        PrecoServicoDetalheRecord(
            id_compra="",
            id_item_compra=1,
            codigo_item_catalogo=2,
        )

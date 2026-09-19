import pytest
from pydantic import ValidationError

from contracts.pgc_agregacao import PgcAgregacaoRecord
from contracts.pgc_detalhe import PgcDetalheRecord


def test_pgc_detalhe_uppercases_text_and_keeps_identity() -> None:
    record = PgcDetalheRecord(
        codigo_uasg="153001",
        nome_uasg=" uasg centro ",
        orgao="36000",
        numero_artefato=12,
        ano_artefato=2026,
        ordem_dfd=1,
        codigo_item_catalogo=449156,
        descricao_item_catalogo=" notebook ",
        ano_pca_projeto_compra=2026,
        quantidade_item=2,
        valor_unitario_item=10,
        valor_total_item=20,
    )
    assert record.codigo_uasg == "153001"
    assert record.nome_uasg == "UASG CENTRO"
    assert record.codigo_item_catalogo == "449156"
    assert record.descricao_item_catalogo == "NOTEBOOK"
    assert record.quantidade_item == 2.0
    assert record.valor_unitario_item == 10.0


def test_pgc_detalhe_rejects_blank_orgao() -> None:
    with pytest.raises(ValidationError):
        PgcDetalheRecord(
            codigo_uasg="153001",
            orgao="  ",
            numero_artefato=1,
            ano_artefato=2026,
            ordem_dfd=0,
            codigo_item_catalogo="1",
            ano_pca_projeto_compra=2026,
        )


def test_pgc_agregacao_uppercases_orgao_fields() -> None:
    record = PgcAgregacaoRecord(
        orgao="36000",
        ano=2026,
        poder=" executivo ",
        esfera=" federal ",
        quantidade_total_itens=3,
        valor_total_estimado=99.5,
    )
    assert record.orgao == "36000"
    assert record.poder == "EXECUTIVO"
    assert record.esfera == "FEDERAL"
    assert record.valor_total_estimado == 99.5


def test_pgc_agregacao_requires_orgao_and_ano() -> None:
    with pytest.raises(ValidationError):
        PgcAgregacaoRecord(orgao="", ano=2026)

import pytest
from pydantic import ValidationError

from contracts.legado_compra_sem_licitacao import LegadoCompraSemLicitacaoRecord
from contracts.legado_item_licitacao import LegadoItemLicitacaoRecord
from contracts.legado_item_pregao import LegadoItemPregaoRecord
from contracts.legado_item_sem_licitacao import LegadoItemSemLicitacaoRecord
from contracts.legado_licitacao import LegadoLicitacaoRecord
from contracts.legado_pregao import LegadoPregaoRecord
from contracts.legado_rdc import LegadoRdcRecord


def test_legado_licitacao_uppercases_text_and_keeps_id() -> None:
    record = LegadoLicitacaoRecord(
        id_compra=123,
        nome_modalidade=" pregao ",
        objeto=" notebook ",
        valor_estimado_total=10,
    )
    assert record.id_compra == "123"
    assert record.nome_modalidade == "PREGAO"
    assert record.objeto == "NOTEBOOK"
    assert record.valor_estimado_total == 10.0


def test_legado_licitacao_rejects_blank_id() -> None:
    with pytest.raises(ValidationError):
        LegadoLicitacaoRecord(id_compra="  ")


def test_legado_item_licitacao_requires_ids() -> None:
    record = LegadoItemLicitacaoRecord(
        id_compra="c1",
        id_compra_item="i1",
        nome_uasg=" uasg ",
        quantidade=2,
    )
    assert record.id_compra_item == "i1"
    assert record.nome_uasg == "UASG"
    assert record.quantidade == 2.0


def test_legado_pregao_parses_string_values() -> None:
    record = LegadoPregaoRecord(
        id_compra="p1",
        no_ausg=" uasg centro ",
        valor_estimado_total="1.50",
        valor_homologado_total="2,25",
    )
    assert record.no_ausg == "UASG CENTRO"
    assert record.valor_estimado_total == 1.5
    assert record.valor_homologado_total == 2.25


def test_legado_item_pregao_parses_string_amounts() -> None:
    record = LegadoItemPregaoRecord(
        id_compra="p1",
        id_compra_item="i1",
        quantidade_item="3",
        valor_homologado_item="10,00",
    )
    assert record.quantidade_item == 3.0
    assert record.valor_homologado_item == 10.0


def test_legado_compra_sem_licitacao_uppercases_objeto() -> None:
    record = LegadoCompraSemLicitacaoRecord(
        id_compra="d1",
        ds_objeto_licitacao=" servico ",
        vr_estimado=9,
    )
    assert record.ds_objeto_licitacao == "SERVICO"
    assert record.vr_estimado == 9.0


def test_legado_item_sem_licitacao_keeps_composite_key() -> None:
    record = LegadoItemSemLicitacaoRecord(
        id_compra="d1",
        id_compra_item="i2",
        no_fornecedor_vencedor=" acme ",
    )
    assert record.id_compra == "d1"
    assert record.no_fornecedor_vencedor == "ACME"


def test_legado_rdc_accepts_numeric_nome_responsavel() -> None:
    record = LegadoRdcRecord(
        identificador="rdc-1",
        nome_responsavel=0,
        uf_uasg=" df ",
        objeto=" obra ",
    )
    assert record.identificador == "rdc-1"
    assert record.nome_responsavel == "0"
    assert record.uf_uasg == "DF"
    assert record.objeto == "OBRA"

"""Ingere consultarItemLicitacao na tabela legado_item_licitacao."""

from typing import Any

from contracts.legado_item_licitacao import LegadoItemLicitacaoRecord
from etl.ingestion.legado.filters import LEGADO_ITEM_MODALIDADES
from etl.ingestion.legado.legado_sql import legado_upsert_sql
from etl.ingestion.legado.map_legado_fields import legado_item_licitacao_fields
from etl.ingestion.legado.query_params import (
    legado_item_licitacao_query_params,
    legado_job_name,
)
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-legado/2_consultarItemLicitacao"
PAGE_SIZE = 100
TABLE_NAME = "legado_item_licitacao"
UPSERT_SQL = legado_upsert_sql(TABLE_NAME)


def map_legado_item_licitacao_row(row: dict[str, Any]) -> LegadoItemLicitacaoRecord:
    """Mapeia um objeto resultado de consultarItemLicitacao.

    Exemplo:
        record = map_legado_item_licitacao_row({"id_compra": "c1", "id_compra_item": "i1"})
    """
    return LegadoItemLicitacaoRecord(**legado_item_licitacao_fields(row))


def main() -> None:
    """Ingere consultarItemLicitacao na tabela legado_item_licitacao."""
    for modalidade in LEGADO_ITEM_MODALIDADES:
        _ingest_item_licitacao(modalidade)


def _ingest_item_licitacao(modalidade: int) -> None:
    """Ingere consultarItemLicitacao da modalidade na tabela legado_item_licitacao."""
    run_page_batch_ingestion(
        logger_name="legado_item_licitacao",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_legado_item_licitacao_row,
        table_name=TABLE_NAME,
        query_params=legado_item_licitacao_query_params(modalidade),
        job_name=legado_job_name("legado_item_licitacao", modalidade),
    )


if __name__ == "__main__":
    main()

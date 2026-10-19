"""Ingere consultarCompraItensSemLicitacao na tabela legado_item_sem_licitacao."""

from typing import Any

from contracts.legado_item_sem_licitacao import LegadoItemSemLicitacaoRecord
from etl.ingestion.full_dump import for_each_dump_year
from etl.ingestion.legado.legado_sql import legado_upsert_sql
from etl.ingestion.legado.map_legado_fields import legado_item_sem_licitacao_fields
from etl.ingestion.legado.query_params import (
    legado_item_sem_licitacao_query_params,
    legado_job_name,
)
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-legado/6_consultarCompraItensSemLicitacao"
PAGE_SIZE = 100
TABLE_NAME = "legado_item_sem_licitacao"
UPSERT_SQL = legado_upsert_sql(TABLE_NAME)


def map_legado_item_sem_licitacao_row(row: dict[str, Any]) -> LegadoItemSemLicitacaoRecord:
    """Mapeia um objeto resultado de consultarCompraItensSemLicitacao.

    Exemplo:
        record = map_legado_item_sem_licitacao_row({"id_compra": "d1", "id_compra_item": "i2"})
    """
    return LegadoItemSemLicitacaoRecord(**legado_item_sem_licitacao_fields(row))


def main() -> None:
    """Ingere consultarCompraItensSemLicitacao na tabela legado_item_sem_licitacao."""
    for_each_dump_year(_ingest_year)


def _ingest_year(ano: int) -> None:
    """Ingere consultarCompraItensSemLicitacao do ano na tabela legado_item_sem_licitacao."""
    run_page_batch_ingestion(
        logger_name="legado_item_sem_licitacao",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_legado_item_sem_licitacao_row,
        table_name=TABLE_NAME,
        query_params=legado_item_sem_licitacao_query_params(ano),
        job_name=legado_job_name("legado_item_sem_licitacao", ano),
    )


if __name__ == "__main__":
    main()

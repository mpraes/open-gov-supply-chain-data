"""Ingere consultarLicitacao na tabela legado_licitacao."""

from typing import Any

from contracts.legado_licitacao import LegadoLicitacaoRecord
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.full_dump import for_each_date_slice
from etl.ingestion.legado.legado_sql import legado_upsert_sql
from etl.ingestion.legado.map_legado_fields import legado_licitacao_fields
from etl.ingestion.legado.query_params import legado_job_name, legado_licitacao_query_params
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-legado/1_consultarLicitacao"
PAGE_SIZE = 100
TABLE_NAME = "legado_licitacao"
UPSERT_SQL = legado_upsert_sql(TABLE_NAME)


def map_legado_licitacao_row(row: dict[str, Any]) -> LegadoLicitacaoRecord:
    """Mapeia um objeto resultado de consultarLicitacao.

    Exemplo:
        record = map_legado_licitacao_row({"id_compra": "123", "objeto": "x"})
    """
    return LegadoLicitacaoRecord(**legado_licitacao_fields(row))


def main() -> None:
    """Ingere consultarLicitacao na tabela legado_licitacao."""
    for_each_date_slice(_ingest_window)


def _ingest_window(inicial: str, final: str) -> None:
    """Ingere consultarLicitacao da janela de publicação na tabela legado_licitacao."""
    run_page_batch_ingestion(
        logger_name="legado_licitacao",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_legado_licitacao_row,
        table_name=TABLE_NAME,
        query_params=legado_licitacao_query_params(inicial, final),
        job_name=legado_job_name("legado_licitacao", inicial, final),
        date_watermark=DateWatermark(
            table=TABLE_NAME,
            column="data_publicacao",
            start_param="data_publicacao_inicial",
            end_param="data_publicacao_final",
        ),
    )


if __name__ == "__main__":
    main()

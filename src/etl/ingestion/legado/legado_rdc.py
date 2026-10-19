"""Ingere consultarRdc na tabela legado_rdc."""

from typing import Any

from contracts.legado_rdc import LegadoRdcRecord
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.full_dump import for_each_date_slice
from etl.ingestion.legado.legado_sql import legado_upsert_sql
from etl.ingestion.legado.map_legado_fields import legado_rdc_fields
from etl.ingestion.legado.query_params import legado_job_name, legado_rdc_query_params
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-legado/7_consultarRdc"
PAGE_SIZE = 100
TABLE_NAME = "legado_rdc"
UPSERT_SQL = legado_upsert_sql(TABLE_NAME)


def map_legado_rdc_row(row: dict[str, Any]) -> LegadoRdcRecord:
    """Mapeia um objeto resultado de consultarRdc.

    Exemplo:
        record = map_legado_rdc_row({"identificador": "rdc-1", "objeto": "x"})
    """
    return LegadoRdcRecord(**legado_rdc_fields(row))


def main() -> None:
    """Ingere consultarRdc na tabela legado_rdc."""
    for_each_date_slice(_ingest_window)


def _ingest_window(inicial: str, final: str) -> None:
    """Ingere consultarRdc da janela de publicação na tabela legado_rdc."""
    run_page_batch_ingestion(
        logger_name="legado_rdc",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_legado_rdc_row,
        table_name=TABLE_NAME,
        query_params=legado_rdc_query_params(inicial, final),
        job_name=legado_job_name("legado_rdc", inicial, final),
        date_watermark=DateWatermark(
            table=TABLE_NAME,
            column="data_publicacao",
            start_param="data_publicacao_min",
            end_param="data_publicacao_max",
        ),
    )


if __name__ == "__main__":
    main()

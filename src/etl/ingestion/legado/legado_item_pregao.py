"""Ingere consultarItensPregoes na tabela legado_item_pregao."""

from typing import Any

from contracts.legado_item_pregao import LegadoItemPregaoRecord
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.full_dump import for_each_date_slice
from etl.ingestion.legado.legado_sql import legado_upsert_sql
from etl.ingestion.legado.map_legado_fields import legado_item_pregao_fields
from etl.ingestion.legado.query_params import (
    legado_item_pregao_query_params,
    legado_job_name,
)
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-legado/4_consultarItensPregoes"
PAGE_SIZE = 100
TABLE_NAME = "legado_item_pregao"
UPSERT_SQL = legado_upsert_sql(TABLE_NAME)


def map_legado_item_pregao_row(row: dict[str, Any]) -> LegadoItemPregaoRecord:
    """Mapeia um objeto resultado de consultarItensPregoes.

    Exemplo:
        record = map_legado_item_pregao_row({"id_compra": "p1", "id_compra_item": "i1"})
    """
    return LegadoItemPregaoRecord(**legado_item_pregao_fields(row))


def main() -> None:
    """Ingere consultarItensPregoes na tabela legado_item_pregao."""
    for_each_date_slice(_ingest_window)


def _ingest_window(inicial: str, final: str) -> None:
    """Ingere consultarItensPregoes da janela de homologação na tabela legado_item_pregao."""
    run_page_batch_ingestion(
        logger_name="legado_item_pregao",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_legado_item_pregao_row,
        table_name=TABLE_NAME,
        query_params=legado_item_pregao_query_params(inicial, final),
        job_name=legado_job_name("legado_item_pregao", inicial, final),
        date_watermark=DateWatermark(
            table=TABLE_NAME,
            column="dt_hom",
            start_param="dt_hom_inicial",
            end_param="dt_hom_final",
        ),
    )


if __name__ == "__main__":
    main()

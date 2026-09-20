from collections.abc import Callable
from logging import Logger
from pathlib import Path
from typing import Any

from clients.compras_api import QueryParams, fetch_one_resultado_page
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.page_runner import FetchOnePage, run_page_batch_ingestion
from etl.ingestion.remaining_columns import TABLE_SPECS
from etl.ingestion.script_runner import DEFAULT_ENV_PATH
from etl.ingestion.upsert_sql import build_upsert_sql
from etl.ingestion.pipeline import MapRow


def run_remaining_ingestion(
    *,
    logger_name: str,
    endpoint_path: str,
    table_name: str,
    map_row: MapRow,
    query_params: QueryParams | None = None,
    job_name: str | None = None,
    page_size: int | None = 100,
    fetch_page_fn: FetchOnePage = fetch_one_resultado_page,
    env_path: Path = DEFAULT_ENV_PATH,
    log: Logger | None = None,
    load_secret: Callable[..., str] | None = None,
    connect_fn: Callable[..., Any] | None = None,
    date_watermark: DateWatermark | None = None,
) -> int:
    """Page-batch ingest one remaining catalog table.

    Example:
        run_remaining_ingestion(
            logger_name="contratacao",
            endpoint_path="/modulo-contratacoes/1_consultarContratacoes_PNCP_14133",
            table_name="contratacao",
            map_row=map_contratacao_row,
            query_params=params,
        )
    """
    columns, conflict = TABLE_SPECS[table_name]
    kwargs: dict[str, Any] = {}
    if load_secret is not None:
        kwargs["load_secret"] = load_secret
    if connect_fn is not None:
        kwargs["connect_fn"] = connect_fn
    return run_page_batch_ingestion(
        logger_name=logger_name,
        endpoint_path=endpoint_path,
        page_size=page_size,
        upsert_sql=build_upsert_sql(table_name, columns, conflict),
        map_row=map_row,
        table_name=table_name,
        env_path=env_path,
        log=log,
        query_params=query_params,
        job_name=job_name if job_name is not None else logger_name,
        fetch_page_fn=fetch_page_fn,
        date_watermark=date_watermark,
        **kwargs,
    )

from collections.abc import Callable
from logging import Logger
from pathlib import Path
from typing import Any

from clients.compras_api import QueryParams, fetch_one_resultado_page
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.iso_date_slices import iso_date_slices
from etl.ingestion.page_runner import FetchOnePage, run_page_batch_ingestion
from etl.ingestion.remaining_columns import TABLE_SPECS
from etl.ingestion.remaining_query_params import slice_job_name
from etl.ingestion.script_runner import DEFAULT_ENV_PATH
from etl.ingestion.upsert_sql import build_upsert_sql
from etl.ingestion.pipeline import MapRow

ParamsForSlice = Callable[[str, str], QueryParams]
RemainingIngest = Callable[..., int]


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
    parallel_pages: int = 1,
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
        parallel_pages=parallel_pages,
        **kwargs,
    )


def run_sliced_remaining_ingestion(
    *,
    data_inicial: str,
    data_final: str,
    params_for_slice: ParamsForSlice,
    job_prefix: str,
    max_days: int = 365,
    run_one: RemainingIngest = run_remaining_ingestion,
    **kwargs: Any,
) -> int:
    """Ingest one table across API date windows of at most `max_days`.

    Example:
        run_sliced_remaining_ingestion(
            data_inicial="2000-01-01", data_final="2026-09-22",
            params_for_slice=arp_query_params, job_prefix="arp",
            logger_name="arp", endpoint_path="/modulo-arp/1_consultarARP",
            table_name="arp", map_row=map_arp_row,
        )
    """
    total = 0
    for inicial, final in iso_date_slices(data_inicial, data_final, max_days=max_days):
        total += _ingest_date_slice(
            run_one, params_for_slice, job_prefix, inicial, final, kwargs
        )
    return total


def _ingest_date_slice(
    run_one: RemainingIngest,
    params_for_slice: ParamsForSlice,
    job_prefix: str,
    inicial: str,
    final: str,
    kwargs: dict[str, Any],
) -> int:
    return run_one(
        query_params=params_for_slice(inicial, final),
        job_name=slice_job_name(job_prefix, inicial, final),
        **kwargs,
    )

from collections.abc import Callable
from logging import Logger
from pathlib import Path
from typing import Any

from clients.compras_api import QueryParams, fetch_one_resultado_page
from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import (
    DateWatermark,
    apply_date_watermark,
    rewrite_job_slice,
)
from etl.ingestion.job_cursor import (
    ensure_job_cursor_table,
    load_job_cursor,
    save_job_cursor,
)
from etl.ingestion.page_loop import run_page_batch_loop
from etl.ingestion.pipeline import MapRow, upsert_mapped_rows
from etl.ingestion.script_runner import (
    BASE_URL,
    DEFAULT_ENV_PATH,
    ConnectPostgresFn,
    LoadSecret,
    _open_connection,
)
from observability.logging_json import get_json_logger, log_info

FetchOnePage = Callable[..., tuple[list[dict[str, Any]], int]]


def run_page_batch_ingestion(
    *,
    logger_name: str,
    endpoint_path: str,
    page_size: int | None,
    upsert_sql: str,
    map_row: MapRow,
    table_name: str,
    env_path: Path = DEFAULT_ENV_PATH,
    base_url: str = BASE_URL,
    log: Logger | None = None,
    load_secret: LoadSecret = load_secret_key_func,
    connect_fn: ConnectPostgresFn | None = None,
    query_params: QueryParams | None = None,
    job_name: str | None = None,
    fetch_page_fn: FetchOnePage = fetch_one_resultado_page,
    date_watermark: DateWatermark | None = None,
    parallel_pages: int = 1,
) -> int:
    """Ingest one API page at a time and persist a resume cursor.

    Example:
        run_page_batch_ingestion(
            logger_name="material_item",
            endpoint_path="/modulo-material/4_consultarItemMaterial",
            page_size=500, upsert_sql=SQL, map_row=map_material_item_row,
            table_name="material_item",
        )
    """
    logger = log if log is not None else get_json_logger(logger_name)
    headers = {"Authorization": load_secret(env_path, "DADOS_GOV_API_KEY")}
    conn = _open_connection(env_path, load_secret, connect_fn)
    url = f"{base_url}{endpoint_path}"
    job = job_name if job_name is not None else logger_name
    try:
        return _run_connected_pages(
            conn=conn,
            url=url,
            headers=headers,
            page_size=page_size,
            upsert_sql=upsert_sql,
            map_row=map_row,
            table_name=table_name,
            log=logger,
            job_name=job,
            query_params=query_params,
            fetch_page_fn=fetch_page_fn,
            date_watermark=date_watermark,
            parallel_pages=parallel_pages,
        )
    finally:
        conn.close()


def _run_connected_pages(
    *,
    conn: Any,
    url: str,
    headers: dict[str, str],
    page_size: int | None,
    upsert_sql: str,
    map_row: MapRow,
    table_name: str,
    log: Logger,
    job_name: str,
    query_params: QueryParams | None,
    fetch_page_fn: FetchOnePage,
    date_watermark: DateWatermark | None,
    parallel_pages: int,
) -> int:
    ensure_job_cursor_table(conn)
    resolved = _resolve_watermark(conn, query_params, job_name, date_watermark, log)
    if resolved is None:
        return 0
    params, job = resolved
    return _loop_api_pages(
        conn=conn,
        url=url,
        headers=headers,
        page_size=page_size,
        upsert_sql=upsert_sql,
        map_row=map_row,
        table_name=table_name,
        log=log,
        job_name=job,
        query_params=params,
        fetch_page_fn=fetch_page_fn,
        parallel_pages=parallel_pages,
    )


def _resolve_watermark(
    conn: Any,
    query_params: QueryParams | None,
    job_name: str,
    date_watermark: DateWatermark | None,
    log: Logger,
) -> tuple[QueryParams | None, str] | None:
    if date_watermark is None:
        return query_params, job_name
    if query_params is None:
        raise ValueError("date_watermark requires query_params with start and end dates")
    original_start = query_params[date_watermark.start_param]
    raised = apply_date_watermark(conn, query_params, date_watermark)
    if raised is None:
        log_info(log, "watermark_caught_up", table=date_watermark.table)
        return None
    if not isinstance(original_start, str):
        raise ValueError(
            f"{date_watermark.start_param} expected str, got {type(original_start).__name__}"
        )
    return raised, rewrite_job_slice(job_name, original_start, str(raised[date_watermark.start_param]))


def _loop_api_pages(
    *,
    conn: Any,
    url: str,
    headers: dict[str, str],
    page_size: int | None,
    upsert_sql: str,
    map_row: MapRow,
    table_name: str,
    log: Logger,
    job_name: str,
    query_params: QueryParams | None,
    fetch_page_fn: FetchOnePage,
    parallel_pages: int,
) -> int:
    return run_page_batch_loop(
        load_cursor=lambda: load_job_cursor(conn, job_name),
        fetch_page=lambda pagina: fetch_page_fn(
            url,
            headers,
            pagina=pagina,
            page_size=page_size,
            query_params=query_params,
            log=log,
        ),
        ingest_rows=lambda rows: upsert_mapped_rows(
            conn, upsert_sql, rows, map_row, log, table_name
        ),
        save_cursor=lambda pagina: save_job_cursor(conn, job_name, pagina),
        log=log,
        job_name=job_name,
        parallel_pages=parallel_pages,
    )

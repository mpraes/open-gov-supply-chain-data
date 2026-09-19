from collections.abc import Callable
from logging import Logger
from pathlib import Path
from typing import Any

from clients.compras_api import QueryParams, fetch_one_resultado_page
from config.load_secret_key import load_secret_key_func
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
from observability.logging_json import get_json_logger

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
        ensure_job_cursor_table(conn)
        return _loop_api_pages(
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
        )
    finally:
        conn.close()


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
) -> int:
    return run_page_batch_loop(
        load_cursor=lambda: load_job_cursor(conn, job_name),
        fetch_page=lambda pagina: fetch_page_fn(
            url,
            headers,
            pagina=pagina,
            page_size=page_size,
            query_params=query_params,
        ),
        ingest_rows=lambda rows: upsert_mapped_rows(
            conn, upsert_sql, rows, map_row, log, table_name
        ),
        save_cursor=lambda pagina: save_job_cursor(conn, job_name, pagina),
        log=log,
        job_name=job_name,
    )

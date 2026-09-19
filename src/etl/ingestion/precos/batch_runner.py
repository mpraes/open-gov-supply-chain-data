from logging import Logger
from pathlib import Path
from typing import Any

from clients.compras_api import CodeParamsFn, fetch_resultado_pages_for_codes
from config.load_secret_key import load_secret_key_func
from etl.ingestion.pipeline import MapRow, run_api_upsert_ingestion
from etl.ingestion.precos.batch_loop import run_code_batch_loop
from etl.ingestion.precos.catalog_codes import list_codes_after
from etl.ingestion.precos.code_cursor import (
    ensure_code_cursor_table,
    load_code_cursor,
    save_code_cursor,
)
from etl.ingestion.precos.code_pages import FetchForCodes, _bind_codigo_fetch_pages
from etl.ingestion.script_runner import (
    BASE_URL,
    DEFAULT_ENV_PATH,
    ConnectPostgresFn,
    LoadSecret,
    _open_connection,
)
from observability.logging_json import get_json_logger

DEFAULT_BATCH_SIZE = 20


def run_preco_batch_ingestion(
    *,
    logger_name: str,
    endpoint_path: str,
    page_size: int | None,
    upsert_sql: str,
    map_row: MapRow,
    table_name: str,
    catalog_table: str,
    catalog_column: str,
    params_for_code: CodeParamsFn,
    batch_size: int = DEFAULT_BATCH_SIZE,
    pause_seconds: float = 1.0,
    job_name: str | None = None,
    env_path: Path = DEFAULT_ENV_PATH,
    base_url: str = BASE_URL,
    log: Logger | None = None,
    load_secret: LoadSecret = load_secret_key_func,
    connect_fn: ConnectPostgresFn | None = None,
    fetch_for_codes: FetchForCodes = fetch_resultado_pages_for_codes,
) -> int:
    """Ingest practiced prices in small catalog-code batches with a resume cursor.

    Example:
        run_preco_batch_ingestion(
            logger_name="preco_material",
            endpoint_path="/modulo-pesquisa-preco/1_consultarMaterial",
            page_size=100, upsert_sql=SQL, map_row=map_preco_material_row,
            table_name="preco_material", catalog_table="material_item",
            catalog_column="cod_item", params_for_code=material_preco_query_params,
        )
    """
    logger = log if log is not None else get_json_logger(logger_name)
    headers = {"Authorization": load_secret(env_path, "DADOS_GOV_API_KEY")}
    conn = _open_connection(env_path, load_secret, connect_fn)
    job = job_name if job_name is not None else logger_name
    url = f"{base_url}{endpoint_path}"
    try:
        ensure_code_cursor_table(conn)
        return _loop_preco_batches(
            conn=conn,
            url=url,
            headers=headers,
            page_size=page_size,
            upsert_sql=upsert_sql,
            map_row=map_row,
            table_name=table_name,
            catalog_table=catalog_table,
            catalog_column=catalog_column,
            params_for_code=params_for_code,
            batch_size=batch_size,
            pause_seconds=pause_seconds,
            job_name=job,
            log=logger,
            fetch_for_codes=fetch_for_codes,
        )
    finally:
        conn.close()


def _loop_preco_batches(
    *,
    conn: Any,
    url: str,
    headers: dict[str, str],
    page_size: int | None,
    upsert_sql: str,
    map_row: MapRow,
    table_name: str,
    catalog_table: str,
    catalog_column: str,
    params_for_code: CodeParamsFn,
    batch_size: int,
    pause_seconds: float,
    job_name: str,
    log: Logger,
    fetch_for_codes: FetchForCodes,
) -> int:
    return run_code_batch_loop(
        load_cursor=lambda: load_code_cursor(conn, job_name),
        next_codes=lambda last, limit: list_codes_after(
            conn,
            table=catalog_table,
            column=catalog_column,
            last_code=last,
            limit=limit,
        ),
        save_cursor=lambda last: save_code_cursor(conn, job_name, last),
        ingest_codes=lambda codes: _ingest_code_batch(
            url=url,
            headers=headers,
            page_size=page_size,
            upsert_sql=upsert_sql,
            map_row=map_row,
            conn=conn,
            log=log,
            table_name=table_name,
            codes=codes,
            params_for_code=params_for_code,
            pause_seconds=pause_seconds,
            fetch_for_codes=fetch_for_codes,
        ),
        batch_size=batch_size,
        log=log,
        job_name=job_name,
    )


def _ingest_code_batch(
    *,
    url: str,
    headers: dict[str, str],
    page_size: int | None,
    upsert_sql: str,
    map_row: MapRow,
    conn: Any,
    log: Logger,
    table_name: str,
    codes: list[int],
    params_for_code: CodeParamsFn,
    pause_seconds: float,
    fetch_for_codes: FetchForCodes,
) -> int:
    fetch_pages = _bind_codigo_fetch_pages(
        codes, params_for_code, fetch_for_codes, pause_seconds
    )
    return run_api_upsert_ingestion(
        url=url,
        headers=headers,
        page_size=page_size,
        upsert_sql=upsert_sql,
        map_row=map_row,
        conn=conn,
        log=log,
        table_name=table_name,
        fetch_pages=fetch_pages,
    )

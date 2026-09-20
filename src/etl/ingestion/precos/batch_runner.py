from collections.abc import Mapping
from logging import Logger
from pathlib import Path
from typing import Any

from clients.compras_api import CodeParamsFn, fetch_resultado_pages_for_codes
from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import with_dest_compra_inicio
from etl.ingestion.pipeline import MapRow, run_api_upsert_ingestion
from etl.ingestion.precos.batch_loop import run_code_batch_loop
from etl.ingestion.precos.catalog_codes import list_codes_after, list_codes_after_absent
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
    dest_code_column: str | None = None,
    stringify_code: bool = False,
    dest_date_column: str = "data_compra",
    absent_dest_table: str | None = None,
    absent_dest_column: str | None = None,
    absent_filters: Mapping[str, str | int] | None = None,
    batch_size: int = DEFAULT_BATCH_SIZE,
    pause_seconds: float = 0,
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
            page_size=500, upsert_sql=SQL, map_row=map_preco_material_row,
            table_name="preco_material", catalog_table="material_pdm",
            catalog_column="cod_pdm", params_for_code=material_preco_query_params,
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
            dest_code_column=dest_code_column,
            stringify_code=stringify_code,
            dest_date_column=dest_date_column,
            absent_dest_table=absent_dest_table,
            absent_dest_column=absent_dest_column,
            absent_filters=absent_filters,
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
    dest_code_column: str | None,
    stringify_code: bool,
    dest_date_column: str,
    absent_dest_table: str | None,
    absent_dest_column: str | None,
    absent_filters: Mapping[str, str | int] | None,
    batch_size: int,
    pause_seconds: float,
    job_name: str,
    log: Logger,
    fetch_for_codes: FetchForCodes,
) -> int:
    total = _run_code_batches(
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
        dest_code_column=dest_code_column,
        stringify_code=stringify_code,
        dest_date_column=dest_date_column,
        absent_dest_table=absent_dest_table,
        absent_dest_column=absent_dest_column,
        absent_filters=absent_filters,
        batch_size=batch_size,
        pause_seconds=pause_seconds,
        job_name=job_name,
        log=log,
        fetch_for_codes=fetch_for_codes,
    )
    save_code_cursor(conn, job_name, 0)
    return total


def _run_code_batches(
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
    dest_code_column: str | None,
    stringify_code: bool,
    dest_date_column: str,
    absent_dest_table: str | None,
    absent_dest_column: str | None,
    absent_filters: Mapping[str, str | int] | None,
    batch_size: int,
    pause_seconds: float,
    job_name: str,
    log: Logger,
    fetch_for_codes: FetchForCodes,
) -> int:
    resolved_params = _resolve_code_params(
        conn, table_name, dest_code_column, stringify_code, dest_date_column, params_for_code
    )
    return run_code_batch_loop(
        load_cursor=lambda: load_code_cursor(conn, job_name),
        next_codes=lambda last, limit: _next_catalog_codes(
            conn,
            catalog_table,
            catalog_column,
            last,
            limit,
            absent_dest_table,
            absent_dest_column,
            absent_filters,
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
            params_for_code=resolved_params,
            pause_seconds=pause_seconds,
            fetch_for_codes=fetch_for_codes,
        ),
        batch_size=batch_size,
        log=log,
        job_name=job_name,
    )


def _next_catalog_codes(
    conn: Any,
    catalog_table: str,
    catalog_column: str,
    last_code: int,
    limit: int,
    absent_dest_table: str | None,
    absent_dest_column: str | None,
    absent_filters: Mapping[str, str | int] | None,
) -> list[int]:
    if absent_dest_table is None or absent_dest_column is None:
        return list_codes_after(
            conn,
            table=catalog_table,
            column=catalog_column,
            last_code=last_code,
            limit=limit,
        )
    filters = dict(absent_filters) if absent_filters is not None else {}
    return list_codes_after_absent(
        conn,
        table=catalog_table,
        column=catalog_column,
        last_code=last_code,
        limit=limit,
        dest_table=absent_dest_table,
        dest_column=absent_dest_column,
        dest_filters=filters,
    )


def _resolve_code_params(
    conn: Any,
    table_name: str,
    dest_code_column: str | None,
    stringify_code: bool,
    dest_date_column: str,
    params_for_code: CodeParamsFn,
) -> CodeParamsFn:
    if dest_code_column is None:
        return params_for_code
    return with_dest_compra_inicio(
        params_for_code,
        conn,
        table_name,
        dest_code_column,
        stringify_code=stringify_code,
        date_column=dest_date_column,
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

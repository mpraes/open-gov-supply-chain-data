from collections.abc import Mapping
from logging import Logger
from pathlib import Path

from clients.compras_api import CodeParamsFn, fetch_resultado_pages_for_codes
from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import with_dest_compra_inicio
from etl.ingestion.pipeline import (
    MapRow,
    SupportsDbConnection,
    run_api_upsert_ingestion,
)
from etl.ingestion.precos.batch_job import (
    PrecoBatchJob,
    PrecoCatalogSpec,
    PrecoFetchSpec,
)
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
DEFAULT_PARALLEL_CODES = 4


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
    parallel_codes: int = DEFAULT_PARALLEL_CODES,
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
    conn = _open_connection(env_path, load_secret, connect_fn)
    try:
        ensure_code_cursor_table(conn)
        return _loop_preco_batches(
            _build_preco_batch_job(
                logger_name=logger_name,
                endpoint_path=endpoint_path,
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
                parallel_codes=parallel_codes,
                job_name=job_name,
                env_path=env_path,
                base_url=base_url,
                log=logger,
                load_secret=load_secret,
                conn=conn,
                fetch_for_codes=fetch_for_codes,
            )
        )
    finally:
        conn.close()


def _loop_preco_batches(job: PrecoBatchJob) -> int:
    total = _run_code_batches(job)
    save_code_cursor(job.conn, job.catalog.job_name, 0)
    return total


def _run_code_batches(job: PrecoBatchJob) -> int:
    catalog = job.catalog
    params_for_code = _resolve_code_params(job)
    return run_code_batch_loop(
        load_cursor=lambda: load_code_cursor(job.conn, catalog.job_name),
        next_codes=lambda last, limit: _next_catalog_codes(job, last, limit),
        save_cursor=lambda last: save_code_cursor(job.conn, catalog.job_name, last),
        ingest_codes=lambda codes: _ingest_code_batch(job, codes, params_for_code),
        batch_size=catalog.batch_size,
        log=job.log,
        job_name=catalog.job_name,
    )


def _next_catalog_codes(job: PrecoBatchJob, last_code: int, limit: int) -> list[int]:
    catalog = job.catalog
    if catalog.absent_dest_table is None or catalog.absent_dest_column is None:
        return list_codes_after(
            job.conn,
            table=catalog.catalog_table,
            column=catalog.catalog_column,
            last_code=last_code,
            limit=limit,
        )
    filters = dict(catalog.absent_filters) if catalog.absent_filters is not None else {}
    return list_codes_after_absent(
        job.conn,
        table=catalog.catalog_table,
        column=catalog.catalog_column,
        last_code=last_code,
        limit=limit,
        dest_table=catalog.absent_dest_table,
        dest_column=catalog.absent_dest_column,
        dest_filters=filters,
    )


def _resolve_code_params(job: PrecoBatchJob) -> CodeParamsFn:
    catalog = job.catalog
    if catalog.dest_code_column is None:
        return catalog.params_for_code
    return with_dest_compra_inicio(
        catalog.params_for_code,
        job.conn,
        job.fetch.table_name,
        catalog.dest_code_column,
        stringify_code=catalog.stringify_code,
        date_column=catalog.dest_date_column,
    )


def _ingest_code_batch(
    job: PrecoBatchJob,
    codes: list[int],
    params_for_code: CodeParamsFn,
) -> int:
    fetch = job.fetch
    fetch_pages = _bind_codigo_fetch_pages(
        codes,
        params_for_code,
        fetch.fetch_for_codes,
        fetch.pause_seconds,
        fetch.parallel_codes,
    )
    return run_api_upsert_ingestion(
        url=fetch.url,
        headers=fetch.headers,
        page_size=fetch.page_size,
        upsert_sql=fetch.upsert_sql,
        map_row=fetch.map_row,
        conn=job.conn,
        log=job.log,
        table_name=fetch.table_name,
        fetch_pages=fetch_pages,
    )


def _build_preco_batch_job(
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
    dest_code_column: str | None,
    stringify_code: bool,
    dest_date_column: str,
    absent_dest_table: str | None,
    absent_dest_column: str | None,
    absent_filters: Mapping[str, str | int] | None,
    batch_size: int,
    pause_seconds: float,
    parallel_codes: int,
    job_name: str | None,
    env_path: Path,
    base_url: str,
    log: Logger,
    load_secret: LoadSecret,
    conn: SupportsDbConnection,
    fetch_for_codes: FetchForCodes,
) -> PrecoBatchJob:
    job = job_name if job_name is not None else logger_name
    return PrecoBatchJob(
        conn=conn,
        log=log,
        fetch=_preco_fetch_spec(
            url=f"{base_url}{endpoint_path}",
            headers={"Authorization": load_secret(env_path, "DADOS_GOV_API_KEY")},
            page_size=page_size,
            upsert_sql=upsert_sql,
            map_row=map_row,
            table_name=table_name,
            pause_seconds=pause_seconds,
            parallel_codes=parallel_codes,
            fetch_for_codes=fetch_for_codes,
        ),
        catalog=_preco_catalog_spec(
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
            job_name=job,
        ),
    )


def _preco_fetch_spec(
    *,
    url: str,
    headers: dict[str, str],
    page_size: int | None,
    upsert_sql: str,
    map_row: MapRow,
    table_name: str,
    pause_seconds: float,
    parallel_codes: int,
    fetch_for_codes: FetchForCodes,
) -> PrecoFetchSpec:
    return PrecoFetchSpec(
        url=url,
        headers=headers,
        page_size=page_size,
        upsert_sql=upsert_sql,
        map_row=map_row,
        table_name=table_name,
        pause_seconds=pause_seconds,
        parallel_codes=parallel_codes,
        fetch_for_codes=fetch_for_codes,
    )


def _preco_catalog_spec(
    *,
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
    job_name: str,
) -> PrecoCatalogSpec:
    return PrecoCatalogSpec(
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
        job_name=job_name,
    )

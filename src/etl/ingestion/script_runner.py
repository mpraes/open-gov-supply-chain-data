from collections.abc import Callable
from logging import Logger
from pathlib import Path
from typing import Any

from config.load_secret_key import load_secret_key_func
from etl.ingestion.db import connect_postgres
from etl.ingestion.pipeline import FetchPages, MapRow, run_api_upsert_ingestion
from observability.logging_json import get_json_logger

BASE_URL = "https://dadosabertos.compras.gov.br"
DEFAULT_ENV_PATH = Path(__file__).resolve().parents[3] / ".env"

LoadSecret = Callable[[Path, str], str]
ConnectPostgresFn = Callable[..., Any]


def run_script_ingestion(
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
    fetch_pages: FetchPages | None = None,
) -> int:
    """Wire secrets + DB for one API upsert ETL script entrypoint.

    Example:
        run_script_ingestion(
            logger_name="material_item",
            endpoint_path="/modulo-material/4_consultarItemMaterial",
            page_size=500,
            upsert_sql=UPSERT_SQL,
            map_row=map_material_item_row,
            table_name="material_item",
        )
    """
    logger = log if log is not None else get_json_logger(logger_name)
    headers = {"Authorization": load_secret(env_path, "DADOS_GOV_API_KEY")}
    conn = _open_connection(env_path, load_secret, connect_fn)
    url = f"{base_url}{endpoint_path}"
    try:
        return _invoke_pipeline(
            url=url,
            headers=headers,
            page_size=page_size,
            upsert_sql=upsert_sql,
            map_row=map_row,
            conn=conn,
            log=logger,
            table_name=table_name,
            fetch_pages=fetch_pages,
        )
    finally:
        conn.close()


def _invoke_pipeline(
    *,
    url: str,
    headers: dict[str, str],
    page_size: int | None,
    upsert_sql: str,
    map_row: MapRow,
    conn: Any,
    log: Logger,
    table_name: str,
    fetch_pages: FetchPages | None,
) -> int:
    if fetch_pages is None:
        return run_api_upsert_ingestion(
            url=url,
            headers=headers,
            page_size=page_size,
            upsert_sql=upsert_sql,
            map_row=map_row,
            conn=conn,
            log=log,
            table_name=table_name,
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


def _open_connection(
    env_path: Path,
    load_secret: LoadSecret,
    connect_fn: ConnectPostgresFn | None,
) -> Any:
    kwargs = {
        "host": load_secret(env_path, "PSQL_HOST"),
        "port": load_secret(env_path, "PSQL_PORT"),
        "user": load_secret(env_path, "PSQL_USER"),
        "password": load_secret(env_path, "PSQL_PASSWORD"),
        "dbname": load_secret(env_path, "PSQL_DB"),
    }
    if connect_fn is not None:
        return connect_fn(**kwargs)
    return connect_postgres(**kwargs)

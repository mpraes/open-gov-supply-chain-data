from collections.abc import Callable, Mapping
from logging import Logger
from time import perf_counter
from typing import Any, Protocol

from psycopg2 import Error as PsycopgError
from pydantic import ValidationError

from clients.compras_api import fetch_all_resultado_pages
from observability.logging_json import log_error, log_info
from observability.timing import fields_since


class SupportsModelDump(Protocol):
    def model_dump(self) -> dict[str, Any]: ...


class SupportsCursorExecute(Protocol):
    def execute(self, sql: str, params: dict[str, Any]) -> None: ...

    def __enter__(self) -> "SupportsCursorExecute": ...

    def __exit__(self, *args: object) -> None: ...


class SupportsDbConnection(Protocol):
    def cursor(self) -> SupportsCursorExecute: ...

    def __enter__(self) -> "SupportsDbConnection": ...

    def __exit__(self, *args: object) -> None: ...


FetchPages = Callable[..., list[dict[str, Any]]]
MapRow = Callable[[dict[str, Any]], SupportsModelDump]


class _UpsertCount:
    """Mutable row counter so DB errors can log rows_done mid-loop."""

    def __init__(self) -> None:
        self.value = 0


def run_api_upsert_ingestion(
    *,
    url: str,
    headers: dict[str, str],
    page_size: int | None,
    upsert_sql: str,
    map_row: MapRow,
    conn: SupportsDbConnection,
    log: Logger,
    table_name: str,
    fetch_pages: FetchPages = fetch_all_resultado_pages,
) -> int:
    """Fetch API pages, map rows, and upsert into Postgres.

    Example:
        n = run_api_upsert_ingestion(
            url=url, headers=headers, page_size=500,
            upsert_sql=SQL, map_row=map_item_row,
            conn=conn, log=log, table_name="material_item",
        )
    """
    rows = _fetch_resultado_rows(url, headers, page_size, log, fetch_pages)
    return upsert_mapped_rows(conn, upsert_sql, rows, map_row, log, table_name)


def upsert_mapped_rows(
    conn: SupportsDbConnection,
    upsert_sql: str,
    rows: list[dict[str, Any]],
    map_row: MapRow,
    log: Logger,
    table_name: str,
) -> int:
    """Map and upsert already-fetched API rows.

    Example:
        n = upsert_mapped_rows(conn, SQL, rows, map_row, log, "material_item")
    """
    return _upsert_mapped_rows(conn, upsert_sql, rows, map_row, log, table_name)


def _fetch_resultado_rows(
    url: str,
    headers: dict[str, str],
    page_size: int | None,
    log: Logger,
    fetch_pages: FetchPages,
) -> list[dict[str, Any]]:
    started = perf_counter()
    try:
        rows = fetch_pages(url, headers, page_size=page_size)
    except Exception as exc:
        log_error(
            log,
            "api_fetch_failed",
            endpoint=url,
            error=str(exc),
            **fields_since(started, 0),
        )
        raise
    _log_api_fetch_ok(log, rows, page_size, fields_since(started, len(rows)))
    return rows


def _log_api_fetch_ok(
    log: Logger,
    rows: list[dict[str, Any]],
    page_size: int | None,
    timing: Mapping[str, int | float],
) -> None:
    if page_size is None:
        log_info(log, "api_fetch_ok", rows=len(rows), **timing)
        return
    log_info(log, "api_fetch_ok", rows=len(rows), page_size=page_size, **timing)


def _upsert_mapped_rows(
    conn: SupportsDbConnection,
    upsert_sql: str,
    rows: list[dict[str, Any]],
    map_row: MapRow,
    log: Logger,
    table_name: str,
) -> int:
    started = perf_counter()
    count = _UpsertCount()
    try:
        _run_upsert_transaction(conn, upsert_sql, rows, map_row, log, table_name, count)
    except PsycopgError as exc:
        log_error(
            log,
            "upsert_failed",
            table=table_name,
            rows_done=count.value,
            error=str(exc),
            **fields_since(started, count.value),
        )
        raise
    log_info(
        log,
        "upsert_ok",
        table=table_name,
        rows=count.value,
        **fields_since(started, count.value),
    )
    return count.value


def _run_upsert_transaction(
    conn: SupportsDbConnection,
    upsert_sql: str,
    rows: list[dict[str, Any]],
    map_row: MapRow,
    log: Logger,
    table_name: str,
    count: _UpsertCount,
) -> None:
    with conn:
        _run_upsert_on_connection(conn, upsert_sql, rows, map_row, log, table_name, count)


def _run_upsert_on_connection(
    conn: SupportsDbConnection,
    upsert_sql: str,
    rows: list[dict[str, Any]],
    map_row: MapRow,
    log: Logger,
    table_name: str,
    count: _UpsertCount,
) -> None:
    with conn.cursor() as cur:
        _upsert_each_row(cur, upsert_sql, rows, map_row, log, table_name, count)


def _upsert_each_row(
    cur: SupportsCursorExecute,
    upsert_sql: str,
    rows: list[dict[str, Any]],
    map_row: MapRow,
    log: Logger,
    table_name: str,
    count: _UpsertCount,
) -> None:
    for row in rows:
        record = _map_row_or_log(row, map_row, log, table_name)
        cur.execute(upsert_sql, record.model_dump())
        count.value += 1


def _map_row_or_log(
    row: dict[str, Any],
    map_row: MapRow,
    log: Logger,
    table_name: str,
) -> SupportsModelDump:
    try:
        return map_row(row)
    except (ValidationError, KeyError) as exc:
        log_error(
            log,
            "row_validation_failed",
            table=table_name,
            error=str(exc),
            offending_row=row,
        )
        raise

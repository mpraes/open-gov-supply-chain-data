"""Busca páginas da API, mapeia as linhas e faz upsert no Postgres."""

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
    """Protocolo de registro com model_dump para o upsert."""

    def model_dump(self) -> dict[str, Any]:
        """Devolve o registro como dicionário de colunas."""
        ...


class SupportsCursorExecute(Protocol):
    """Protocolo do cursor que executa o SQL de upsert."""

    def execute(self, sql: str, params: dict[str, Any]) -> None:
        """Executa o SQL de upsert com os parâmetros da linha."""
        ...

    def __enter__(self) -> "SupportsCursorExecute":
        """Abre o cursor para o bloco de upsert."""
        ...

    def __exit__(self, *args: object) -> None:
        """Encerra o cursor ao sair do bloco."""
        ...


class SupportsDbConnection(Protocol):
    """Protocolo da conexão que abre cursor e confirma a transação."""

    def cursor(self) -> SupportsCursorExecute:
        """Abre um cursor para o upsert."""
        ...

    def close(self) -> None:
        """Fecha a conexão Postgres."""
        ...

    def __enter__(self) -> "SupportsDbConnection":
        """Entra na transação da conexão."""
        ...

    def __exit__(self, *args: object) -> None:
        """Encerra a transação da conexão."""
        ...


FetchPages = Callable[..., list[dict[str, Any]]]
MapRow = Callable[[dict[str, Any]], SupportsModelDump]


class _UpsertCount:
    """Contador mutável de linhas para o log de rows_done quando um erro de banco interrompe o laço."""

    def __init__(self) -> None:
        """Zera o contador de linhas já gravadas."""
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
    """Busca páginas da API, mapeia as linhas e faz upsert no Postgres.

    Exemplo:
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
    """Mapeia e faz upsert das linhas da API já buscadas.

    Exemplo:
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
    """Busca as páginas da API, registra api_fetch_ok e relança api_fetch_failed."""
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
    """Registra api_fetch_ok com rows e, quando informado, page_size."""
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
    """Faz o upsert na transação, registra upsert_ok e relança upsert_failed."""
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
    """Executa o upsert no bloco de transação da conexão."""
    with conn:
        _run_upsert_on_connection(
            conn, upsert_sql, rows, map_row, log, table_name, count
        )


def _run_upsert_on_connection(
    conn: SupportsDbConnection,
    upsert_sql: str,
    rows: list[dict[str, Any]],
    map_row: MapRow,
    log: Logger,
    table_name: str,
    count: _UpsertCount,
) -> None:
    """Abre o cursor e grava cada linha mapeada."""
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
    """Mapeia cada linha, executa o SQL de upsert e incrementa o contador."""
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
    """Mapeia a linha ou registra row_validation_failed e relança ValidationError ou KeyError."""
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

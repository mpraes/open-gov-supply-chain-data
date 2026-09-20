from collections.abc import Callable
from logging import Logger
from time import perf_counter
from typing import Any

from observability.logging_json import log_info
from observability.timing import fields_since

LoadCursor = Callable[[], int]
FetchPage = Callable[[int], tuple[list[dict[str, Any]], int]]
IngestRows = Callable[[list[dict[str, Any]]], int]
SaveCursor = Callable[[int], None]


def run_page_batch_loop(
    *,
    load_cursor: LoadCursor,
    fetch_page: FetchPage,
    ingest_rows: IngestRows,
    save_cursor: SaveCursor,
    log: Logger,
    job_name: str,
) -> int:
    """Fetch and persist one API page at a time, advancing a resume cursor.

    Example:
        total = run_page_batch_loop(
            load_cursor=load, fetch_page=fetch, ingest_rows=upsert,
            save_cursor=save, log=log, job_name="material_item",
        )
    """
    total = 0
    pagina = load_cursor() + 1
    started = perf_counter()
    while True:
        page_started = perf_counter()
        rows, total_pages = fetch_page(pagina)
        if total_pages == 0 or pagina > total_pages:
            _log_page_batches_done(log, job_name, total, started)
            return total
        total += _ingest_page_and_checkpoint(
            pagina, rows, total_pages, ingest_rows, save_cursor, log, job_name, page_started
        )
        if pagina >= total_pages:
            _log_page_batches_done(log, job_name, total, started)
            return total
        pagina += 1


def _log_page_batches_done(log: Logger, job_name: str, total: int, started: float) -> None:
    log_info(
        log,
        "page_batches_done",
        job=job_name,
        rows=total,
        **fields_since(started, total),
    )


def _ingest_page_and_checkpoint(
    pagina: int,
    rows: list[dict[str, Any]],
    total_pages: int,
    ingest_rows: IngestRows,
    save_cursor: SaveCursor,
    log: Logger,
    job_name: str,
    started: float,
) -> int:
    batch_rows = ingest_rows(rows)
    save_cursor(pagina)
    log_info(
        log,
        "page_batch_ok",
        job=job_name,
        page=pagina,
        total_pages=total_pages,
        rows=batch_rows,
        **fields_since(started, batch_rows),
    )
    return batch_rows

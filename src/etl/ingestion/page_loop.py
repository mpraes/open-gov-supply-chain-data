from collections.abc import Callable
from logging import Logger
from typing import Any

from observability.logging_json import log_info

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
    while True:
        rows, total_pages = fetch_page(pagina)
        if total_pages == 0 or pagina > total_pages:
            log_info(log, "page_batches_done", job=job_name, rows=total)
            return total
        total += _ingest_page_and_checkpoint(
            pagina, rows, total_pages, ingest_rows, save_cursor, log, job_name
        )
        if pagina >= total_pages:
            log_info(log, "page_batches_done", job=job_name, rows=total)
            return total
        pagina += 1


def _ingest_page_and_checkpoint(
    pagina: int,
    rows: list[dict[str, Any]],
    total_pages: int,
    ingest_rows: IngestRows,
    save_cursor: SaveCursor,
    log: Logger,
    job_name: str,
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
    )
    return batch_rows

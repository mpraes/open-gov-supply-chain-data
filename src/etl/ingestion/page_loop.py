"""Busca páginas da API em paralelo e persiste cada uma antes de avançar o cursor."""

from collections.abc import Callable
from concurrent.futures import Future, ThreadPoolExecutor
from logging import Logger
from time import perf_counter
from typing import Any

from observability.logging_json import log_info
from observability.timing import fields_since

LoadCursor = Callable[[], int]
FetchPage = Callable[[int], tuple[list[dict[str, Any]], int]]
IngestRows = Callable[[list[dict[str, Any]]], int]
SaveCursor = Callable[[int], None]
PageFuture = Future[tuple[list[dict[str, Any]], int]]


class _FetchWindow:
    """Guarda as páginas submetidas, a próxima a buscar e o total já conhecido."""

    def __init__(self, next_fetch: int) -> None:
        """Inicia a janela vazia na página next_fetch."""
        self.pending: dict[int, PageFuture] = {}
        self.next_fetch = next_fetch
        self.total_pages: int | None = None


def run_page_batch_loop(
    *,
    load_cursor: LoadCursor,
    fetch_page: FetchPage,
    ingest_rows: IngestRows,
    save_cursor: SaveCursor,
    log: Logger,
    job_name: str,
    parallel_pages: int = 1,
) -> int:
    """Busca e persiste uma página da API por vez, avançando o cursor de retomada.

    Exemplo:
        total = run_page_batch_loop(
            load_cursor=load, fetch_page=fetch, ingest_rows=upsert,
            save_cursor=save, log=log, job_name="material_item",
        )
    """
    _require_parallel_pages(parallel_pages)
    started = perf_counter()
    window = _FetchWindow(load_cursor() + 1)
    with ThreadPoolExecutor(max_workers=parallel_pages) as pool:
        try:
            return _loop_pending_pages(
                window=window,
                fetch_page=fetch_page,
                ingest_rows=ingest_rows,
                save_cursor=save_cursor,
                log=log,
                job_name=job_name,
                parallel_pages=parallel_pages,
                pool=pool,
                started=started,
            )
        finally:
            _cancel_pending(window)


def _require_parallel_pages(parallel_pages: int) -> None:
    """Recusa parallel_pages menor que 1."""
    if parallel_pages < 1:
        raise ValueError(f"parallel_pages expected int >= 1, got {parallel_pages!r}")


def _loop_pending_pages(
    *,
    window: _FetchWindow,
    fetch_page: FetchPage,
    ingest_rows: IngestRows,
    save_cursor: SaveCursor,
    log: Logger,
    job_name: str,
    parallel_pages: int,
    pool: ThreadPoolExecutor,
    started: float,
) -> int:
    """Ingere cada página pronta em ordem, grava o cursor e encerra ao atingir total_pages."""
    total = 0
    while True:
        _fill_fetch_window(window, pool, fetch_page, parallel_pages)
        ready = _take_ready_page(window)
        if ready is None:
            _log_page_batches_done(log, job_name, total, started)
            return total
        pagina, rows, total_pages, page_started = ready
        _fill_fetch_window(window, pool, fetch_page, parallel_pages)
        total += _ingest_page_and_checkpoint(
            pagina, rows, total_pages, ingest_rows, save_cursor, log, job_name, page_started
        )
        if pagina >= total_pages:
            _log_page_batches_done(log, job_name, total, started)
            return total


def _fill_fetch_window(
    window: _FetchWindow,
    pool: ThreadPoolExecutor,
    fetch_page: FetchPage,
    parallel_pages: int,
) -> None:
    """Submete fetch_page até encher a janela ou passar de total_pages."""
    while len(window.pending) < parallel_pages:
        if window.total_pages is not None and window.next_fetch > window.total_pages:
            return
        if window.total_pages is None and window.pending:
            return
        window.pending[window.next_fetch] = pool.submit(fetch_page, window.next_fetch)
        window.next_fetch += 1


def _take_ready_page(
    window: _FetchWindow,
) -> tuple[int, list[dict[str, Any]], int, float] | None:
    """Aguarda a menor página pendente e devolve linhas, total_pages e o instante."""
    if not window.pending:
        return None
    pagina = min(window.pending)
    page_started = perf_counter()
    rows, total_pages = window.pending.pop(pagina).result()
    window.total_pages = total_pages
    if total_pages == 0 or pagina > total_pages:
        return None
    return pagina, rows, total_pages, page_started


def _cancel_pending(window: _FetchWindow) -> None:
    """Cancela e esvazia as páginas ainda pendentes."""
    for future in window.pending.values():
        future.cancel()
    window.pending.clear()


def _log_page_batches_done(log: Logger, job_name: str, total: int, started: float) -> None:
    """Registra page_batches_done com job, rows e o tempo decorrido."""
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
    """Persiste a página, grava o cursor em pagina e registra page_batch_ok."""
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

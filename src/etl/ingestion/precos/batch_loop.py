"""Percorre lotes de códigos de catálogo, persiste cada lote e avança o cursor."""

from collections.abc import Callable
from logging import Logger
from time import perf_counter

from observability.logging_json import log_info
from observability.timing import fields_since

LoadCursor = Callable[[], int]
NextCodes = Callable[[int, int], list[int]]
SaveCursor = Callable[[int], None]
IngestCodes = Callable[[list[int]], int]


def run_code_batch_loop(
    *,
    load_cursor: LoadCursor,
    next_codes: NextCodes,
    save_cursor: SaveCursor,
    ingest_codes: IngestCodes,
    batch_size: int,
    log: Logger,
    job_name: str,
) -> int:
    """Busca e persiste lotes de códigos de catálogo, avançando o cursor de retomada.

    Exemplo:
        total = run_code_batch_loop(
            load_cursor=load, next_codes=next_batch, save_cursor=save,
            ingest_codes=ingest, batch_size=20, log=log, job_name="preco_material",
        )
    """
    total = 0
    started = perf_counter()
    while True:
        codes = next_codes(load_cursor(), batch_size)
        if not codes:
            log_info(
                log,
                "preco_batches_done",
                job=job_name,
                rows=total,
                **fields_since(started, total),
            )
            return total
        total += _ingest_and_checkpoint(codes, ingest_codes, save_cursor, log, job_name)


def _ingest_and_checkpoint(
    codes: list[int],
    ingest_codes: IngestCodes,
    save_cursor: SaveCursor,
    log: Logger,
    job_name: str,
) -> int:
    """Persiste o lote, grava o último código no cursor e retorna as linhas gravadas."""
    started = perf_counter()
    batch_rows = ingest_codes(codes)
    save_cursor(codes[-1])
    log_info(
        log,
        "preco_batch_ok",
        job=job_name,
        last_code=codes[-1],
        codes=len(codes),
        rows=batch_rows,
        **fields_since(started, batch_rows),
    )
    return batch_rows

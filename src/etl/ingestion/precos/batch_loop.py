from collections.abc import Callable
from logging import Logger

from observability.logging_json import log_info

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
    """Fetch and persist catalog-code batches, advancing a resume cursor.

    Example:
        total = run_code_batch_loop(
            load_cursor=load, next_codes=next_batch, save_cursor=save,
            ingest_codes=ingest, batch_size=20, log=log, job_name="preco_material",
        )
    """
    total = 0
    while True:
        codes = next_codes(load_cursor(), batch_size)
        if not codes:
            log_info(log, "preco_batches_done", job=job_name, rows=total)
            return total
        total += _ingest_and_checkpoint(codes, ingest_codes, save_cursor, log, job_name)


def _ingest_and_checkpoint(
    codes: list[int],
    ingest_codes: IngestCodes,
    save_cursor: SaveCursor,
    log: Logger,
    job_name: str,
) -> int:
    batch_rows = ingest_codes(codes)
    save_cursor(codes[-1])
    log_info(
        log,
        "preco_batch_ok",
        job=job_name,
        last_code=codes[-1],
        codes=len(codes),
        rows=batch_rows,
    )
    return batch_rows

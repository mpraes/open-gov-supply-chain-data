from time import perf_counter


def timing_fields(*, duration_s: float, rows: int) -> dict[str, int | float]:
    """Build duration_ms and optional rows_per_sec for a JSON log event.

    Example:
        timing_fields(duration_s=2.5, rows=100)
        == {"duration_ms": 2500, "rows_per_sec": 40.0}
    """
    duration_ms = int(round(max(duration_s, 0.0) * 1000))
    fields: dict[str, int | float] = {"duration_ms": duration_ms}
    if rows > 0 and duration_s > 0:
        fields["rows_per_sec"] = round(rows / duration_s, 1)
    return fields


def fields_since(
    started: float,
    rows: int,
    now: float | None = None,
) -> dict[str, int | float]:
    """Time a span from `started` (perf_counter) to now.

    Example:
        started = perf_counter()
        ...
        log_info(log, "upsert_ok", rows=n, **fields_since(started, n))
    """
    end = now if now is not None else perf_counter()
    return timing_fields(duration_s=max(end - started, 0.0), rows=rows)

"""Campos de duração e throughput para eventos de log JSON."""

from time import perf_counter


def timing_fields(*, duration_s: float, rows: int) -> dict[str, int | float]:
    """Monta duration_ms e, quando há linhas, rows_per_sec para um evento de log JSON.

    Exemplo:
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
    """Mede o intervalo de `started` (perf_counter) até agora.

    Exemplo:
        started = perf_counter()
        ...
        log_info(log, "upsert_ok", rows=n, **fields_since(started, n))
    """
    end = now if now is not None else perf_counter()
    return timing_fields(duration_s=max(end - started, 0.0), rows=rows)

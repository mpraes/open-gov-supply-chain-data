"""Divide uma janela YYYY-MM-DD em fatias inclusivas de no máximo max_days."""

from datetime import date, timedelta


def iso_date_slices(
    inicial: str, final: str, *, max_days: int = 365
) -> list[tuple[str, str]]:
    """Divide uma janela YYYY-MM-DD em fatias inclusivas de no máximo max_days.

    Exemplo:
        iso_date_slices("2024-01-01", "2025-01-01")
    """
    start = _parse_iso(inicial, "inicial")
    end = _parse_iso(final, "final")
    _require_ordered_window(start, end, inicial, final)
    return _walk_slices(start, end, max_days)


def _parse_iso(raw: str, label: str) -> date:
    """Converte o texto para date e recusa o que não for YYYY-MM-DD."""
    try:
        return date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"{label} expected YYYY-MM-DD, got {raw!r}") from exc


def _require_ordered_window(
    start: date, end: date, inicial: str, final: str
) -> None:
    """Recusa a janela em que inicial é posterior a final."""
    if start > end:
        raise ValueError(
            f"expected inicial <= final, got inicial={inicial!r} final={final!r}"
        )


def _walk_slices(start: date, end: date, max_days: int) -> list[tuple[str, str]]:
    """Monta fatias inclusivas de no máximo max_days de start até end."""
    slices: list[tuple[str, str]] = []
    cursor = start
    while cursor <= end:
        slice_end = min(cursor + timedelta(days=max_days), end)
        slices.append((cursor.isoformat(), slice_end.isoformat()))
        cursor = slice_end + timedelta(days=1)
    return slices

"""Percorre a janela completa de carga, de 2000-01-01 até hoje, por ano ou por fatia."""

from collections.abc import Callable
from datetime import date

from etl.ingestion.iso_date_slices import iso_date_slices

FULL_DUMP_START = date(2000, 1, 1)
DateSliceFn = Callable[[str, str], None]
YearFn = Callable[[int], None]


def full_dump_dates(*, today: date | None = None) -> tuple[str, str]:
    """Janela ISO de 2000-01-01 até `today`.

    Exemplo:
        full_dump_dates(today=date(2026, 10, 19)) == ("2000-01-01", "2026-10-19")
    """
    day = _today(today)
    return FULL_DUMP_START.isoformat(), day.isoformat()


def full_dump_years(*, today: date | None = None) -> tuple[int, ...]:
    """Cada ano-calendário de 2000 até `today`.

    Exemplo:
        full_dump_years(today=date(2001, 6, 1)) == (2000, 2001)
    """
    day = _today(today)
    return tuple(range(FULL_DUMP_START.year, day.year + 1))


def for_each_dump_year(visit: YearFn, *, today: date | None = None) -> None:
    """Chama `visit` uma vez por ano da carga completa.

    Exemplo:
        for_each_dump_year(load_year, today=date(2001, 6, 1))
    """
    for ano in full_dump_years(today=today):
        visit(ano)


def for_each_date_slice(visit: DateSliceFn, *, today: date | None = None) -> None:
    """Chama `visit` uma vez por fatia, no tamanho da API, da janela de carga completa.

    Exemplo:
        for_each_date_slice(load_window, today=date(2001, 1, 1))
    """
    inicial, final = full_dump_dates(today=today)
    for start, end in iso_date_slices(inicial, final):
        visit(start, end)


def _today(today: date | None) -> date:
    """Devolve today ou date.today() quando o argumento é None."""
    if today is not None:
        return today
    return date.today()

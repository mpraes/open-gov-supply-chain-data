from datetime import date

from etl.ingestion.full_dump import (
    for_each_date_slice,
    for_each_dump_year,
    full_dump_dates,
    full_dump_years,
)


def test_full_dump_dates_cover_2000_through_today() -> None:
    assert full_dump_dates(today=date(2026, 10, 19)) == ("2000-01-01", "2026-10-19")


def test_full_dump_years_include_every_year_from_2000() -> None:
    years = full_dump_years(today=date(2026, 10, 19))
    assert years[0] == 2000
    assert years[-1] == 2026
    assert len(years) == 27


def test_for_each_dump_year_visits_each_year_once() -> None:
    seen: list[int] = []
    for_each_dump_year(seen.append, today=date(2001, 6, 1))
    assert seen == [2000, 2001]


def test_for_each_date_slice_splits_the_full_window() -> None:
    seen: list[tuple[str, str]] = []
    for_each_date_slice(lambda start, end: seen.append((start, end)), today=date(2001, 1, 1))
    assert seen[0] == ("2000-01-01", "2000-12-31")
    assert seen[-1][1] == "2001-01-01"

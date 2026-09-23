import pytest

from etl.ingestion.iso_date_slices import iso_date_slices


def test_iso_date_slices_keeps_window_within_max_days() -> None:
    assert iso_date_slices("2025-01-01", "2025-06-30") == [("2025-01-01", "2025-06-30")]


def test_iso_date_slices_keeps_exact_max_day_span() -> None:
    assert iso_date_slices("2025-01-01", "2026-01-01") == [("2025-01-01", "2026-01-01")]


def test_iso_date_slices_splits_leap_year_plus_one_day() -> None:
    assert iso_date_slices("2024-01-01", "2025-01-01") == [
        ("2024-01-01", "2024-12-31"),
        ("2025-01-01", "2025-01-01"),
    ]


def test_iso_date_slices_covers_full_dump_without_overlap() -> None:
    slices = iso_date_slices("2000-01-01", "2002-01-01")
    assert slices[0] == ("2000-01-01", "2000-12-31")
    assert slices[1] == ("2001-01-01", "2002-01-01")
    assert slices[-1][1] == "2002-01-01"


def test_iso_date_slices_rejects_inverted_window() -> None:
    with pytest.raises(ValueError, match="2026-09-22"):
        iso_date_slices("2026-09-22", "2000-01-01")

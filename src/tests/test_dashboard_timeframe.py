import pytest

from dashboard.kpis.timeframe import fact_predicate, parse_timeframe


def test_parse_timeframe_accepts_all_and_12m() -> None:
    assert parse_timeframe("all") == "all"
    assert parse_timeframe("12m") == "12m"


def test_parse_timeframe_rejects_unknown_value() -> None:
    with pytest.raises(ValueError, match=r"got 'year'"):
        parse_timeframe("year")


def test_fact_predicate_all_is_true() -> None:
    assert fact_predicate("all") == "TRUE"


def test_fact_predicate_12m_filters_data_compra() -> None:
    sql = fact_predicate("12m")
    assert "data_compra" in sql
    assert "12 months" in sql
    assert sql != "TRUE"

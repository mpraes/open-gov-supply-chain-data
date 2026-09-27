from fakes.analytics_db import FakeAnalyticsConnection

from dashboard.kpis.sql_fetch import fetch_one_row, fetch_rows


def test_fetch_one_row_returns_first_queued_row() -> None:
    conn = FakeAnalyticsConnection(result_sets=[[(7,)]])
    assert fetch_one_row(conn, "SELECT 1") == (7,)
    assert conn.cursor_obj.queries == ["SELECT 1"]


def test_fetch_rows_returns_queued_set() -> None:
    conn = FakeAnalyticsConnection(result_sets=[[("SP", 10), ("RJ", 4)]])
    assert fetch_rows(conn, "SELECT uf") == [("SP", 10), ("RJ", 4)]


def test_fetch_one_row_none_when_empty() -> None:
    conn = FakeAnalyticsConnection(result_sets=[[]])
    assert fetch_one_row(conn, "SELECT 1") is None

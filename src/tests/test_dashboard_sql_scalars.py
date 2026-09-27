from fakes.analytics_db import FakeAnalyticsConnection

from dashboard.kpis.sql_scalars import four_ints, scalar_float, scalar_int


def test_four_ints_casts_row() -> None:
    assert four_ints((1, 2, 3, 4)) == (1, 2, 3, 4)


def test_four_ints_none_is_zeros() -> None:
    assert four_ints(None) == (0, 0, 0, 0)


def test_scalar_float_reads_first_column() -> None:
    conn = FakeAnalyticsConnection(result_sets=[[(99.5,)]])
    assert scalar_float(conn, "SELECT 99.5") == 99.5


def test_scalar_float_empty_is_zero() -> None:
    conn = FakeAnalyticsConnection(result_sets=[[]])
    assert scalar_float(conn, "SELECT 1") == 0.0


def test_scalar_int_reads_first_column() -> None:
    conn = FakeAnalyticsConnection(result_sets=[[(12,)]])
    assert scalar_int(conn, "SELECT 12") == 12


def test_scalar_int_empty_is_zero() -> None:
    conn = FakeAnalyticsConnection(result_sets=[[]])
    assert scalar_int(conn, "SELECT 1") == 0

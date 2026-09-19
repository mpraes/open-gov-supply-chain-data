import pytest

from etl.ingestion.precos.catalog_codes import list_int_column


class FakeCatalogCursor:
    def __init__(self, rows: list[tuple[object, ...]]) -> None:
        self._rows = rows
        self.sql: str | None = None

    def execute(self, sql: str, params: object = None) -> None:
        self.sql = sql
        self.params = params

    def fetchall(self) -> list[tuple[object, ...]]:
        return self._rows

    def __enter__(self) -> "FakeCatalogCursor":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakeCatalogConnection:
    def __init__(self, cursor: FakeCatalogCursor) -> None:
        self.cursor_obj = cursor

    def cursor(self) -> FakeCatalogCursor:
        return self.cursor_obj


def test_list_int_column_returns_codes_in_query_order() -> None:
    cursor = FakeCatalogCursor([(10,), (20,)])
    conn = FakeCatalogConnection(cursor)
    codes = list_int_column(conn, "SELECT cod_item FROM material_item ORDER BY cod_item")
    assert codes == [10, 20]
    assert cursor.sql == "SELECT cod_item FROM material_item ORDER BY cod_item"


def test_list_int_column_returns_empty_list_when_no_rows() -> None:
    conn = FakeCatalogConnection(FakeCatalogCursor([]))
    assert list_int_column(conn, "SELECT cod_item FROM material_item") == []


def test_list_int_column_rejects_row_that_is_not_a_1_tuple() -> None:
    conn = FakeCatalogConnection(FakeCatalogCursor([(10, 20)]))
    with pytest.raises(ValueError, match="expected catalog code row\\[0\\] to be a 1-tuple"):
        list_int_column(conn, "SELECT cod_item, nome FROM material_item")


def test_list_int_column_rejects_non_int_code() -> None:
    conn = FakeCatalogConnection(FakeCatalogCursor([("10",)]))
    with pytest.raises(ValueError, match="expected catalog code row\\[0\\]\\[0\\] to be int"):
        list_int_column(conn, "SELECT cod_item FROM material_item")


def test_list_int_column_forwards_query_params() -> None:
    cursor = FakeCatalogCursor([(21,)])
    conn = FakeCatalogConnection(cursor)
    codes = list_int_column(
        conn,
        "SELECT cod_item FROM material_item WHERE cod_item > %(last_code)s",
        {"last_code": 10, "limit": 2},
    )
    assert codes == [21]
    assert cursor.params == {"last_code": 10, "limit": 2}

import pytest

from etl.ingestion.precos.catalog_codes import list_codes_after


class FakeCatalogCursor:
    def __init__(self, rows: list[tuple[object, ...]]) -> None:
        self._rows = rows
        self.sql: str | None = None
        self.params: object = None

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


def test_list_codes_after_pages_catalog_ids() -> None:
    cursor = FakeCatalogCursor([(11,), (12,)])
    codes = list_codes_after(
        FakeCatalogConnection(cursor),
        table="material_item",
        column="cod_item",
        last_code=10,
        limit=2,
    )
    assert codes == [11, 12]
    assert cursor.params == {"last_code": 10, "limit": 2}
    assert cursor.sql is not None
    assert "material_item" in cursor.sql
    assert "cod_item > %(last_code)s" in cursor.sql


def test_list_codes_after_rejects_unsafe_identifier() -> None:
    conn = FakeCatalogConnection(FakeCatalogCursor([]))
    with pytest.raises(ValueError, match="table expected snake_case identifier"):
        list_codes_after(conn, table="material_item;drop", column="cod_item", last_code=0, limit=1)

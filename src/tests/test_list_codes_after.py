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


def test_list_codes_after_absent_excludes_dest_matches() -> None:
    from etl.ingestion.precos.catalog_codes import list_codes_after_absent

    cursor = FakeCatalogCursor([(11,)])
    codes = list_codes_after_absent(
        FakeCatalogConnection(cursor),
        table="material_class",
        column="cod_classe",
        last_code=10,
        limit=2,
        dest_table="pgc_detalhe_catalogo",
        dest_column="codigo_classe_material",
        dest_filters={"ano_artefato": 2026},
    )
    assert codes == [11]
    assert cursor.params == {"last_code": 10, "limit": 2, "ano_artefato": 2026}
    assert cursor.sql is not None
    assert "NOT EXISTS" in cursor.sql
    assert "pgc_detalhe_catalogo" in cursor.sql
    assert "codigo_classe_material" in cursor.sql
    assert "ano_artefato = %(ano_artefato)s" in cursor.sql

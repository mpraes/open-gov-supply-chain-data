import pytest

from etl.ingestion.arp.missing_keys import (
    missing_ata_headers,
    missing_ata_item_triples,
    resolve_empenho_keys,
    resolve_item_keys,
    table_has_rows,
)


class FakeKeyCursor:
    def __init__(self, rows: list[tuple[object, ...]]) -> None:
        self.rows = rows
        self.sql: str | None = None
        self.params: object = None

    def execute(self, sql: str, params: object = None) -> None:
        self.sql = sql
        self.params = params

    def fetchall(self) -> list[tuple[object, ...]]:
        return self.rows

    def fetchone(self) -> tuple[object, ...] | None:
        if not self.rows:
            return None
        return self.rows[0]

    def __enter__(self) -> "FakeKeyCursor":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakeKeyConnection:
    def __init__(self, cursor: FakeKeyCursor) -> None:
        self.cursor_obj = cursor

    def cursor(self) -> FakeKeyCursor:
        return self.cursor_obj


def test_missing_ata_headers_anti_joins_empenho() -> None:
    cursor = FakeKeyCursor([("10", "36000")])
    got = missing_ata_headers(FakeKeyConnection(cursor), child_table="arp_empenho")
    assert got == [("10", "36000")]
    assert cursor.sql is not None
    assert "FROM arp " in cursor.sql
    assert "arp_empenho" in cursor.sql
    assert "NOT EXISTS" in cursor.sql


def test_missing_ata_item_triples_anti_joins_child() -> None:
    cursor = FakeKeyCursor([("10", "36000", "1")])
    got = missing_ata_item_triples(
        FakeKeyConnection(cursor), child_table="arp_unidade_item"
    )
    assert got == [("10", "36000", "1")]
    assert cursor.sql is not None
    assert "FROM arp_item " in cursor.sql
    assert "arp_unidade_item" in cursor.sql
    assert "numero_item" in cursor.sql


def test_missing_ata_headers_rejects_unknown_child() -> None:
    conn = FakeKeyConnection(FakeKeyCursor([]))
    with pytest.raises(ValueError, match="child_table expected"):
        missing_ata_headers(conn, child_table="arp;drop")


def test_table_has_rows_true_when_fetchone_returns() -> None:
    conn = FakeKeyConnection(FakeKeyCursor([(1,)]))
    assert table_has_rows(conn, "arp") is True


def test_table_has_rows_false_when_empty() -> None:
    conn = FakeKeyConnection(FakeKeyCursor([]))
    assert table_has_rows(conn, "arp") is False


def test_resolve_empenho_keys_falls_back_when_arp_empty() -> None:
    conn = FakeKeyConnection(FakeKeyCursor([]))
    assert resolve_empenho_keys(conn, ("ata", "ug")) == [("ata", "ug")]


def test_resolve_item_keys_falls_back_when_arp_item_empty() -> None:
    conn = FakeKeyConnection(FakeKeyCursor([]))
    assert resolve_item_keys(conn, "arp_unidade_item", ("ata", "ug", "1")) == [
        ("ata", "ug", "1")
    ]

from etl.ingestion.precos.code_cursor import (
    ensure_code_cursor_table,
    load_code_cursor,
    save_code_cursor,
)


class FakeCursorCursor:
    def __init__(self, fetchone_row: tuple[object, ...] | None = None) -> None:
        self.fetchone_row = fetchone_row
        self.execute_calls: list[tuple[str, object]] = []

    def execute(self, sql: str, params: object = None) -> None:
        self.execute_calls.append((sql, params))

    def fetchone(self) -> tuple[object, ...] | None:
        return self.fetchone_row

    def __enter__(self) -> "FakeCursorCursor":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakeCursorConnection:
    def __init__(self, cursor: FakeCursorCursor) -> None:
        self.cursor_obj = cursor
        self.commit_calls = 0

    def cursor(self) -> FakeCursorCursor:
        return self.cursor_obj

    def commit(self) -> None:
        self.commit_calls += 1


def test_load_code_cursor_returns_zero_when_missing() -> None:
    conn = FakeCursorConnection(FakeCursorCursor(None))
    assert load_code_cursor(conn, "preco_material") == 0


def test_load_code_cursor_returns_stored_code() -> None:
    conn = FakeCursorConnection(FakeCursorCursor((38473,)))
    assert load_code_cursor(conn, "preco_material") == 38473


def test_save_code_cursor_upserts_and_commits() -> None:
    cursor = FakeCursorCursor()
    conn = FakeCursorConnection(cursor)
    save_code_cursor(conn, "preco_material", 20)
    assert conn.commit_calls == 1
    assert cursor.execute_calls[0][1] == {"job_name": "preco_material", "last_code": 20}


def test_ensure_code_cursor_table_creates_and_commits() -> None:
    cursor = FakeCursorCursor()
    conn = FakeCursorConnection(cursor)
    ensure_code_cursor_table(conn)
    assert conn.commit_calls == 1
    assert "staging.etl_code_cursor" in cursor.execute_calls[0][0]

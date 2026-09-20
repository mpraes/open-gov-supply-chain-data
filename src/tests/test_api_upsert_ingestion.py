import json
from pathlib import Path
from typing import Any

import pytest
from pydantic import BaseModel, ValidationError
from psycopg2 import Error as PsycopgError

from etl.ingestion.pipeline import run_api_upsert_ingestion
from observability.logging_json import get_json_logger


def _info_events(tmp_path: Path, logger_name: str) -> list[dict[str, object]]:
    path = tmp_path / f"{logger_name}_info.log"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


def _assert_timed(event: dict[str, object], rows: int) -> None:
    assert isinstance(event["duration_ms"], int)
    assert event["duration_ms"] >= 0
    if rows > 0 and event["duration_ms"] > 0:
        assert isinstance(event["rows_per_sec"], float)


class SampleRecord(BaseModel):
    cod: int
    nome: str


class FakeCursor:
    """Named fake cursor that records execute calls."""

    def __init__(self, *, fail_on_call: int | None = None) -> None:
        self.execute_calls: list[tuple[str, dict[str, Any]]] = []
        self._fail_on_call = fail_on_call

    def execute(self, sql: str, params: dict[str, Any]) -> None:
        next_index = len(self.execute_calls) + 1
        if self._fail_on_call is not None and next_index == self._fail_on_call:
            raise PsycopgError("upsert blew up")
        self.execute_calls.append((sql, params))

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakeConnection:
    """Named fake connection exposing a context-managed cursor."""

    def __init__(self, cursor: FakeCursor | None = None) -> None:
        self.cursor_obj = cursor if cursor is not None else FakeCursor()

    def cursor(self) -> FakeCursor:
        return self.cursor_obj

    def __enter__(self) -> "FakeConnection":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakeFetchPages:
    """Named fake that returns canned API rows or raises."""

    def __init__(
        self,
        rows: list[dict[str, Any]] | None = None,
        *,
        error: Exception | None = None,
    ) -> None:
        self._rows = rows if rows is not None else []
        self._error = error
        self.calls: list[dict[str, Any]] = []

    def __call__(
        self,
        url: str,
        headers: dict[str, str],
        *,
        page_size: int | None = 500,
    ) -> list[dict[str, Any]]:
        self.calls.append({"url": url, "headers": headers, "page_size": page_size})
        if self._error is not None:
            raise self._error
        return self._rows


def _map_sample_row(row: dict[str, Any]) -> SampleRecord:
    return SampleRecord(cod=row["codigo"], nome=row["nome"])


def test_run_api_upsert_ingestion_upserts_all_rows(tmp_path: Any) -> None:
    conn = FakeConnection()
    log = get_json_logger("pipeline_upsert_ok", log_dir=tmp_path)
    fetch = FakeFetchPages(
        [{"codigo": 1, "nome": "alpha"}, {"codigo": 2, "nome": "beta"}]
    )
    sql = "INSERT INTO sample VALUES (%(cod)s, %(nome)s)"

    count = run_api_upsert_ingestion(
        url="https://example/x",
        headers={"Authorization": "k"},
        page_size=500,
        upsert_sql=sql,
        map_row=_map_sample_row,
        conn=conn,
        log=log,
        table_name="sample",
        fetch_pages=fetch,
    )

    assert count == 2
    assert fetch.calls == [
        {"url": "https://example/x", "headers": {"Authorization": "k"}, "page_size": 500}
    ]
    assert conn.cursor_obj.execute_calls == [
        (sql, {"cod": 1, "nome": "alpha"}),
        (sql, {"cod": 2, "nome": "beta"}),
    ]
    events = {row["message"]: row for row in _info_events(tmp_path, "pipeline_upsert_ok")}
    _assert_timed(events["api_fetch_ok"], 2)
    _assert_timed(events["upsert_ok"], 2)
    assert events["api_fetch_ok"]["rows"] == 2
    assert events["upsert_ok"]["rows"] == 2


def test_run_api_upsert_ingestion_raises_on_fetch_failure(tmp_path: Any) -> None:
    conn = FakeConnection()
    log = get_json_logger("pipeline_fetch_fail", log_dir=tmp_path)
    fetch = FakeFetchPages(error=RuntimeError("network down"))

    with pytest.raises(RuntimeError, match="network down"):
        run_api_upsert_ingestion(
            url="https://example/x",
            headers={},
            page_size=None,
            upsert_sql="SQL",
            map_row=_map_sample_row,
            conn=conn,
            log=log,
            table_name="sample",
            fetch_pages=fetch,
        )


def test_run_api_upsert_ingestion_raises_on_row_mapping_failure(tmp_path: Any) -> None:
    conn = FakeConnection()
    log = get_json_logger("pipeline_map_fail", log_dir=tmp_path)
    fetch = FakeFetchPages([{"codigo": "bad", "nome": "x"}])

    with pytest.raises(ValidationError):
        run_api_upsert_ingestion(
            url="https://example/x",
            headers={},
            page_size=50,
            upsert_sql="SQL",
            map_row=_map_sample_row,
            conn=conn,
            log=log,
            table_name="sample",
            fetch_pages=fetch,
        )
    assert conn.cursor_obj.execute_calls == []


def test_run_api_upsert_ingestion_raises_on_db_failure(tmp_path: Any) -> None:
    conn = FakeConnection(FakeCursor(fail_on_call=1))
    log = get_json_logger("pipeline_db_fail", log_dir=tmp_path)
    fetch = FakeFetchPages([{"codigo": 1, "nome": "a"}])

    with pytest.raises(PsycopgError, match="upsert blew up"):
        run_api_upsert_ingestion(
            url="https://example/x",
            headers={},
            page_size=50,
            upsert_sql="SQL",
            map_row=_map_sample_row,
            conn=conn,
            log=log,
            table_name="sample",
            fetch_pages=fetch,
        )

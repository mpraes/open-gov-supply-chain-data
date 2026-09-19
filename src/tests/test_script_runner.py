from typing import Any
from pathlib import Path

import pytest

from etl.ingestion.script_runner import run_script_ingestion
from observability.logging_json import get_json_logger


class FakeCursor:
    def __init__(self) -> None:
        self.execute_calls: list[tuple[str, dict[str, Any]]] = []

    def execute(self, sql: str, params: dict[str, Any]) -> None:
        self.execute_calls.append((sql, params))

    def __enter__(self) -> "FakeCursor":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakeConnection:
    def __init__(self) -> None:
        self.cursor_obj = FakeCursor()
        self.closed = False

    def cursor(self) -> FakeCursor:
        return self.cursor_obj

    def close(self) -> None:
        self.closed = True

    def __enter__(self) -> "FakeConnection":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakeConnectPostgres:
    def __init__(self, conn: FakeConnection) -> None:
        self._conn = conn
        self.calls: list[dict[str, str]] = []

    def __call__(self, **kwargs: str) -> FakeConnection:
        self.calls.append(dict(kwargs))
        return self._conn


class FakeFetchPages:
    def __init__(self, rows: list[dict[str, Any]]) -> None:
        self._rows = rows

    def __call__(
        self,
        url: str,
        headers: dict[str, str],
        *,
        page_size: int | None = 500,
    ) -> list[dict[str, Any]]:
        return self._rows


class SampleRecord:
    def __init__(self, cod: int) -> None:
        self._cod = cod

    def model_dump(self) -> dict[str, Any]:
        return {"cod": self._cod}


def test_run_script_ingestion_closes_connection(tmp_path: Path) -> None:
    conn = FakeConnection()
    connect = FakeConnectPostgres(conn)
    log = get_json_logger("script_runner_ok", log_dir=tmp_path)

    def load_secret(_env_path: Path, name: str) -> str:
        return {
            "DADOS_GOV_API_KEY": "api-key",
            "PSQL_HOST": "localhost",
            "PSQL_PORT": "5432",
            "PSQL_USER": "u",
            "PSQL_PASSWORD": "p",
            "PSQL_DB": "db",
        }[name]

    count = run_script_ingestion(
        logger_name="script_runner_ok",
        endpoint_path="/modulo-material/x",
        page_size=10,
        upsert_sql="SQL",
        map_row=lambda row: SampleRecord(row["codigo"]),
        table_name="sample",
        env_path=tmp_path / ".env",
        log=log,
        load_secret=load_secret,
        connect_fn=connect,
        fetch_pages=FakeFetchPages([{"codigo": 7}]),
    )

    assert count == 1
    assert conn.closed is True
    assert connect.calls[0]["host"] == "localhost"
    assert conn.cursor_obj.execute_calls[0][1] == {"cod": 7}


def test_run_script_ingestion_uses_build_fetch_pages(tmp_path: Path) -> None:
    conn = FakeConnection()
    connect = FakeConnectPostgres(conn)
    log = get_json_logger("script_runner_build_fetch", log_dir=tmp_path)
    builders: list[FakeConnection] = []

    def load_secret(_env_path: Path, name: str) -> str:
        return "x"

    def build_fetch_pages(opened: FakeConnection) -> FakeFetchPages:
        builders.append(opened)
        return FakeFetchPages([{"codigo": 3}])

    count = run_script_ingestion(
        logger_name="script_runner_build_fetch",
        endpoint_path="/modulo-pesquisa-preco/x",
        page_size=10,
        upsert_sql="SQL",
        map_row=lambda row: SampleRecord(row["codigo"]),
        table_name="preco_material",
        env_path=tmp_path / ".env",
        log=log,
        load_secret=load_secret,
        connect_fn=connect,
        build_fetch_pages=build_fetch_pages,
    )

    assert count == 1
    assert builders == [conn]
    assert conn.cursor_obj.execute_calls[0][1] == {"cod": 3}
    assert conn.closed is True


def test_run_script_ingestion_closes_connection_on_fetch_error(tmp_path: Path) -> None:
    conn = FakeConnection()
    connect = FakeConnectPostgres(conn)
    log = get_json_logger("script_runner_fail", log_dir=tmp_path)

    def load_secret(_env_path: Path, name: str) -> str:
        return "x"

    def boom(
        url: str,
        headers: dict[str, str],
        *,
        page_size: int | None = 500,
    ) -> list[dict[str, Any]]:
        raise RuntimeError("fetch failed")

    with pytest.raises(RuntimeError, match="fetch failed"):
        run_script_ingestion(
            logger_name="script_runner_fail",
            endpoint_path="/x",
            page_size=None,
            upsert_sql="SQL",
            map_row=lambda row: SampleRecord(1),
            table_name="sample",
            env_path=tmp_path / ".env",
            log=log,
            load_secret=load_secret,
            connect_fn=connect,
            fetch_pages=boom,
        )
    assert conn.closed is True

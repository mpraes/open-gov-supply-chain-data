from pathlib import Path
from typing import Any

from etl.ingestion.page_runner import run_page_batch_ingestion
from observability.logging_json import get_json_logger


class FakePageCursor:
    def __init__(self) -> None:
        self.execute_calls: list[tuple[str, object]] = []

    def execute(self, sql: str, params: object = None) -> None:
        self.execute_calls.append((sql, params))

    def fetchone(self) -> None:
        return None

    def __enter__(self) -> "FakePageCursor":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakePageConnection:
    def __init__(self) -> None:
        self.cursor_obj = FakePageCursor()
        self.closed = False
        self.commit_calls = 0

    def cursor(self) -> FakePageCursor:
        return self.cursor_obj

    def commit(self) -> None:
        self.commit_calls += 1

    def close(self) -> None:
        self.closed = True

    def __enter__(self) -> "FakePageConnection":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakeConnectPostgres:
    def __init__(self, conn: FakePageConnection) -> None:
        self._conn = conn

    def __call__(self, **kwargs: str) -> FakePageConnection:
        return self._conn


class SampleRecord:
    def __init__(self, cod: int) -> None:
        self._cod = cod

    def model_dump(self) -> dict[str, Any]:
        return {"cod": self._cod}


def test_run_page_batch_ingestion_closes_connection_on_empty_catalog(tmp_path: Path) -> None:
    conn = FakePageConnection()
    log = get_json_logger("page_runner_ok", log_dir=tmp_path)

    def load_secret(_env_path: Path, name: str) -> str:
        return "x"

    def empty_page(
        url: str,
        headers: dict[str, str],
        *,
        pagina: int,
        page_size: int | None = 500,
        query_params: dict[str, str | int | bool] | None = None,
    ) -> tuple[list[dict[str, Any]], int]:
        return [], 0

    count = run_page_batch_ingestion(
        logger_name="page_runner_ok",
        endpoint_path="/modulo-material/x",
        page_size=10,
        upsert_sql="SQL",
        map_row=lambda row: SampleRecord(row["codigo"]),
        table_name="sample",
        env_path=tmp_path / ".env",
        log=log,
        load_secret=load_secret,
        connect_fn=FakeConnectPostgres(conn),
        fetch_page_fn=empty_page,
    )
    assert count == 0
    assert conn.closed is True
    assert conn.commit_calls >= 1


def test_run_page_batch_ingestion_forwards_query_params(tmp_path: Path) -> None:
    conn = FakePageConnection()
    log = get_json_logger("page_runner_params", log_dir=tmp_path)
    seen: list[dict[str, str | int | bool] | None] = []

    def load_secret(_env_path: Path, name: str) -> str:
        return "x"

    def capture_page(
        url: str,
        headers: dict[str, str],
        *,
        pagina: int,
        page_size: int | None = 500,
        query_params: dict[str, str | int | bool] | None = None,
    ) -> tuple[list[dict[str, Any]], int]:
        seen.append(query_params)
        return [], 0

    run_page_batch_ingestion(
        logger_name="page_runner_params",
        endpoint_path="/modulo-pgc/1_consultarPgcDetalhe",
        page_size=10,
        upsert_sql="SQL",
        map_row=lambda row: SampleRecord(row["codigo"]),
        table_name="sample",
        env_path=tmp_path / ".env",
        log=log,
        load_secret=load_secret,
        connect_fn=FakeConnectPostgres(conn),
        query_params={"orgao": "36000", "anoPcaProjetoCompra": 2026},
        job_name="pgc_detalhe:36000:2026",
        fetch_page_fn=capture_page,
    )
    assert seen == [{"orgao": "36000", "anoPcaProjetoCompra": 2026}]

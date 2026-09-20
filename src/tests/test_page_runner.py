import json
from pathlib import Path
from typing import Any

from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.page_runner import run_page_batch_ingestion
from observability.logging_json import get_json_logger


class FakePageCursor:
    def __init__(self, dest_max: object = None) -> None:
        self.execute_calls: list[tuple[str, object]] = []
        self.dest_max = dest_max
        self._last_sql = ""

    def execute(self, sql: str, params: object = None) -> None:
        self._last_sql = sql
        self.execute_calls.append((sql, params))

    def fetchone(self) -> tuple[object] | None:
        if "MAX(" in self._last_sql:
            if self.dest_max is None:
                return (None,)
            return (self.dest_max,)
        return None

    def __enter__(self) -> "FakePageCursor":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakePageConnection:
    def __init__(self, dest_max: object = None) -> None:
        self.cursor_obj = FakePageCursor(dest_max)
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


def _stub_secret(_env_path: Path, name: str) -> str:
    return "x"


def test_run_page_batch_ingestion_raises_start_from_dest(tmp_path: Path) -> None:
    conn = FakePageConnection(dest_max="2024-06-15")
    seen: list[dict[str, str | int | bool] | None] = []
    log = get_json_logger("page_runner_watermark", log_dir=tmp_path)

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
        logger_name="page_runner_watermark",
        endpoint_path="/modulo-contratacoes/1",
        page_size=10,
        upsert_sql="SQL",
        map_row=lambda row: SampleRecord(row["codigo"]),
        table_name="contratacao",
        env_path=tmp_path / ".env",
        log=log,
        load_secret=_stub_secret,
        connect_fn=FakeConnectPostgres(conn),
        query_params={
            "dataPublicacaoPncpInicial": "2024-01-01",
            "dataPublicacaoPncpFinal": "2024-12-31",
        },
        job_name="contratacao:2024-01-01:2024-12-31",
        date_watermark=DateWatermark(
            table="contratacao",
            column="data_publicacao_pncp",
            start_param="dataPublicacaoPncpInicial",
            end_param="dataPublicacaoPncpFinal",
        ),
        fetch_page_fn=capture_page,
    )
    assert seen == [
        {
            "dataPublicacaoPncpInicial": "2024-06-15",
            "dataPublicacaoPncpFinal": "2024-12-31",
        }
    ]
    job_params = [params for _sql, params in conn.cursor_obj.execute_calls if isinstance(params, dict) and "job_name" in params]
    assert any(row["job_name"] == "contratacao:2024-06-15:2024-12-31" for row in job_params)


def test_run_page_batch_ingestion_skips_fetch_when_caught_up(tmp_path: Path) -> None:
    conn = FakePageConnection(dest_max="2025-01-01")
    fetched = 0
    log = get_json_logger("page_runner_caught_up", log_dir=tmp_path)

    def capture_page(
        url: str,
        headers: dict[str, str],
        *,
        pagina: int,
        page_size: int | None = 500,
        query_params: dict[str, str | int | bool] | None = None,
    ) -> tuple[list[dict[str, Any]], int]:
        nonlocal fetched
        fetched += 1
        return [], 0

    count = run_page_batch_ingestion(
        logger_name="page_runner_caught_up",
        endpoint_path="/modulo-contratacoes/1",
        page_size=10,
        upsert_sql="SQL",
        map_row=lambda row: SampleRecord(row["codigo"]),
        table_name="contratacao",
        env_path=tmp_path / ".env",
        log=log,
        load_secret=_stub_secret,
        connect_fn=FakeConnectPostgres(conn),
        query_params={
            "dataPublicacaoPncpInicial": "2024-01-01",
            "dataPublicacaoPncpFinal": "2024-12-31",
        },
        job_name="contratacao:2024-01-01:2024-12-31",
        date_watermark=DateWatermark(
            table="contratacao",
            column="data_publicacao_pncp",
            start_param="dataPublicacaoPncpInicial",
            end_param="dataPublicacaoPncpFinal",
        ),
        fetch_page_fn=capture_page,
    )
    assert count == 0
    assert fetched == 0
    events = [
        json.loads(line)
        for line in (tmp_path / "page_runner_caught_up_info.log").read_text(encoding="utf-8").splitlines()
    ]
    assert any(row["message"] == "watermark_caught_up" for row in events)

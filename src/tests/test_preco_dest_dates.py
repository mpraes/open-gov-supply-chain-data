from pathlib import Path

from clients.compras_api import CodeParamsFn
from clients.compras_types import JsonRow
from etl.ingestion.dest_watermark import with_dest_compra_inicio
from etl.ingestion.precos.batch_runner import run_preco_batch_ingestion
from observability.logging_json import get_json_logger


class FakeCompraCursor:
    def __init__(self, value: object) -> None:
        self.value = value
        self.sql: str | None = None
        self.params: object = None

    def execute(self, sql: str, params: object = None) -> None:
        self.sql = sql
        self.params = params

    def fetchone(self) -> tuple[object] | None:
        if self.value is None:
            return (None,)
        return (self.value,)

    def __enter__(self) -> "FakeCompraCursor":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakeCompraConnection:
    def __init__(self, cursor: FakeCompraCursor) -> None:
        self.cursor_obj = cursor

    def cursor(self) -> FakeCompraCursor:
        return self.cursor_obj


def test_with_dest_compra_inicio_adds_date_when_dest_has_rows() -> None:
    cursor = FakeCompraCursor("2024-06-15 10:00:00")
    wrapped = with_dest_compra_inicio(
        lambda code: {"tipo": "codigoPdm", "codigo": str(code)},
        FakeCompraConnection(cursor),
        table="preco_material",
        code_column="codigo_pdm",
        stringify_code=True,
    )
    assert wrapped(123) == {
        "tipo": "codigoPdm",
        "codigo": "123",
        "dataCompraInicio": "2024-06-15",
    }
    assert cursor.params == {"codigo_pdm": "123"}


def test_with_dest_compra_inicio_omits_date_when_dest_empty() -> None:
    cursor = FakeCompraCursor(None)
    wrapped = with_dest_compra_inicio(
        lambda code: {"codigoItemCatalogo": code},
        FakeCompraConnection(cursor),
        table="preco_servico",
        code_column="codigo_item_catalogo",
    )
    assert wrapped(7250) == {"codigoItemCatalogo": 7250}


class FakePrecoCursor:
    def __init__(self, codes: list[int], dest_max: str | None) -> None:
        self.codes = codes
        self.dest_max = dest_max
        self.sql = ""
        self.params: object = None
        self.saved: list[int] = []

    def execute(self, sql: str, params: object = None) -> None:
        self.sql = sql
        self.params = params
        if isinstance(params, dict) and "job_name" in params and "last_code" in params:
            self.saved.append(int(params["last_code"]))

    def fetchone(self) -> tuple[object] | None:
        if "MAX(" in self.sql:
            return (self.dest_max,)
        if self.saved:
            return (self.saved[-1],)
        return None

    def fetchall(self) -> list[tuple[int, ...]]:
        if not isinstance(self.params, dict) or "last_code" not in self.params:
            return []
        last = int(self.params["last_code"])
        limit = int(self.params["limit"])
        remaining = [code for code in self.codes if code > last][:limit]
        return [(code,) for code in remaining]

    def __enter__(self) -> "FakePrecoCursor":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakePrecoConnection:
    def __init__(self, cursor: FakePrecoCursor) -> None:
        self.cursor_obj = cursor
        self.closed = False
        self.commit_calls = 0

    def cursor(self) -> FakePrecoCursor:
        return self.cursor_obj

    def commit(self) -> None:
        self.commit_calls += 1

    def close(self) -> None:
        self.closed = True

    def __enter__(self) -> "FakePrecoConnection":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakePrecoConnect:
    def __init__(self, conn: FakePrecoConnection) -> None:
        self._conn = conn

    def __call__(self, **kwargs: str) -> FakePrecoConnection:
        return self._conn


class SamplePrecoRecord:
    def model_dump(self) -> dict[str, int]:
        return {"id": 1}


class RecordingPrecoFetchForCodes:
    """Named fake that captures params_for_code for the first catalog code."""

    def __init__(self) -> None:
        self.calls: list[dict[str, str | int | bool]] = []

    def __call__(
        self,
        url: str,
        headers: dict[str, str],
        *,
        codes: list[int],
        params_for_code: CodeParamsFn,
        page_size: int | None = 500,
        pause_seconds: float = 0,
        parallel_codes: int = 1,
    ) -> list[JsonRow]:
        captured: dict[str, str | int | bool] = dict(params_for_code(codes[0]))
        captured["parallel_codes"] = parallel_codes
        self.calls.append(captured)
        return []


def test_run_preco_batch_ingestion_filters_by_dest_compra_and_resets_cursor(
    tmp_path: Path,
) -> None:
    cursor = FakePrecoCursor([10], "2024-03-01")
    conn = FakePrecoConnection(cursor)
    fetch_for_codes = RecordingPrecoFetchForCodes()
    run_preco_batch_ingestion(
        logger_name="preco_dest",
        endpoint_path="/modulo-pesquisa-preco/1_consultarMaterial",
        page_size=10,
        upsert_sql="SQL",
        map_row=lambda row: SamplePrecoRecord(),
        table_name="preco_material",
        catalog_table="material_pdm",
        catalog_column="cod_pdm",
        params_for_code=lambda code: {"tipo": "codigoPdm", "codigo": str(code)},
        dest_code_column="codigo_pdm",
        stringify_code=True,
        batch_size=20,
        env_path=tmp_path / ".env",
        log=get_json_logger("preco_dest", log_dir=tmp_path),
        load_secret=lambda _env, _name: "x",
        connect_fn=FakePrecoConnect(conn),
        fetch_for_codes=fetch_for_codes,
    )
    assert fetch_for_codes.calls == [
        {
            "tipo": "codigoPdm",
            "codigo": "10",
            "dataCompraInicio": "2024-03-01",
            "parallel_codes": 4,
        }
    ]
    assert cursor.saved[-1] == 0

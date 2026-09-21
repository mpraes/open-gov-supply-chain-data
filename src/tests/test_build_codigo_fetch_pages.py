from clients.compras_api import CodeParamsFn
from clients.compras_types import JsonRow
from etl.ingestion.precos.code_pages import build_codigo_fetch_pages


class FakeCatalogCursor:
    def __init__(self, rows: list[tuple[object, ...]]) -> None:
        self._rows = rows

    def execute(self, sql: str) -> None:
        return None

    def fetchall(self) -> list[tuple[object, ...]]:
        return self._rows

    def __enter__(self) -> "FakeCatalogCursor":
        return self

    def __exit__(self, *args: object) -> None:
        return None


class FakeCatalogConnection:
    def __init__(self, rows: list[tuple[object, ...]]) -> None:
        self.cursor_obj = FakeCatalogCursor(rows)

    def cursor(self) -> FakeCatalogCursor:
        return self.cursor_obj

    def close(self) -> None:
        return None


class RecordingFetchForCodes:
    """Named fake that records fetch_for_codes kwargs for one catalog code."""

    def __init__(self) -> None:
        self.calls: list[dict[str, object]] = []

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
        self.calls.append(
            {
                "url": url,
                "headers": headers,
                "codes": codes,
                "page_size": page_size,
                "pause_seconds": pause_seconds,
                "parallel_codes": parallel_codes,
                "params": params_for_code(codes[0]),
            }
        )
        return [{"idCompra": 1}]


def test_build_codigo_fetch_pages_loads_codes_and_forwards_page_size() -> None:
    fetch_for_codes = RecordingFetchForCodes()
    fetch_pages = build_codigo_fetch_pages(
        FakeCatalogConnection([(7,)]),
        "SELECT cod_item FROM material_item",
        lambda code: {"tipo": "codigoItemCatalogo", "codigo": str(code)},
        fetch_for_codes=fetch_for_codes,
        parallel_codes=4,
    )
    rows = fetch_pages(
        "https://example.test/preco", {"Authorization": "k"}, page_size=40
    )
    assert rows == [{"idCompra": 1}]
    assert fetch_for_codes.calls == [
        {
            "url": "https://example.test/preco",
            "headers": {"Authorization": "k"},
            "codes": [7],
            "page_size": 40,
            "pause_seconds": 0,
            "parallel_codes": 4,
            "params": {"tipo": "codigoItemCatalogo", "codigo": "7"},
        }
    ]

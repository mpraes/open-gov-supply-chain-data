from typing import Any

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


def test_build_codigo_fetch_pages_loads_codes_and_forwards_page_size() -> None:
    captured: list[dict[str, Any]] = []

    def fake_fetch_for_codes(
        url: str,
        headers: dict[str, str],
        *,
        codes: list[int],
        params_for_code: Any,
        page_size: int | None = 500,
        pause_seconds: float = 0,
    ) -> list[dict[str, Any]]:
        captured.append(
            {
                "url": url,
                "headers": headers,
                "codes": codes,
                "page_size": page_size,
                "pause_seconds": pause_seconds,
                "params": params_for_code(codes[0]),
            }
        )
        return [{"idCompra": 1}]

    fetch_pages = build_codigo_fetch_pages(
        FakeCatalogConnection([(7,)]),
        "SELECT cod_item FROM material_item",
        lambda code: {"tipo": "codigoItemCatalogo", "codigo": str(code)},
        fetch_for_codes=fake_fetch_for_codes,
    )
    rows = fetch_pages("https://example.test/preco", {"Authorization": "k"}, page_size=40)
    assert rows == [{"idCompra": 1}]
    assert captured == [
        {
            "url": "https://example.test/preco",
            "headers": {"Authorization": "k"},
            "codes": [7],
            "page_size": 40,
            "pause_seconds": 0,
            "params": {"tipo": "codigoItemCatalogo", "codigo": "7"},
        }
    ]

from typing import Any

from clients.compras_api import fetch_resultado_pages_for_codes


class FakeResponse:
    def __init__(self, payload: dict[str, Any], status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"http error status={self.status_code}")

    def json(self) -> dict[str, Any]:
        return self._payload


class FakeHttpGetByCodigo:
    """Named fake that returns one page keyed by the `codigo` query param."""

    def __init__(self, pages_by_codigo: dict[str, dict[str, Any]]) -> None:
        self._pages_by_codigo = pages_by_codigo
        self.calls: list[dict[str, Any]] = []

    def __call__(
        self,
        url: str,
        *,
        headers: dict[str, str],
        params: dict[str, str | int | bool],
        timeout: int,
    ) -> FakeResponse:
        self.calls.append({"url": url, "headers": headers, "params": params, "timeout": timeout})
        codigo = str(params["codigo"])
        return FakeResponse(self._pages_by_codigo[codigo])


def test_fetch_resultado_pages_for_codes_concatenates_each_code() -> None:
    http_get = FakeHttpGetByCodigo(
        {
            "10": {
                "resultado": [{"idCompra": 1}],
                "totalPaginas": 1,
                "paginasRestantes": 0,
            },
            "20": {
                "resultado": [{"idCompra": 2}],
                "totalPaginas": 1,
                "paginasRestantes": 0,
            },
        }
    )
    rows = fetch_resultado_pages_for_codes(
        "https://example.test/preco",
        {"Authorization": "key"},
        codes=[10, 20],
        params_for_code=lambda code: {"tipo": "codigoItemCatalogo", "codigo": str(code)},
        page_size=50,
        http_get=http_get,
    )
    assert rows == [{"idCompra": 1}, {"idCompra": 2}]
    assert [call["params"]["codigo"] for call in http_get.calls] == ["10", "20"]
    assert all(call["params"]["tamanhoPagina"] == 50 for call in http_get.calls)


def test_fetch_resultado_pages_for_codes_skips_empty_code_and_continues() -> None:
    http_get = FakeHttpGetByCodigo(
        {
            "10": {
                "resultado": [],
                "totalPaginas": 0,
                "paginasRestantes": 0,
            },
            "20": {
                "resultado": [{"idCompra": 2}],
                "totalPaginas": 1,
                "paginasRestantes": 0,
            },
        }
    )
    rows = fetch_resultado_pages_for_codes(
        "https://example.test/preco",
        {"Authorization": "key"},
        codes=[10, 20],
        params_for_code=lambda code: {"tipo": "codigoItemCatalogo", "codigo": str(code)},
        http_get=http_get,
    )
    assert rows == [{"idCompra": 2}]
    assert [call["params"]["codigo"] for call in http_get.calls] == ["10", "20"]


def test_fetch_resultado_pages_for_codes_returns_empty_when_no_codes() -> None:
    http_get = FakeHttpGetByCodigo({})
    rows = fetch_resultado_pages_for_codes(
        "https://example.test/preco",
        {"Authorization": "key"},
        codes=[],
        params_for_code=lambda code: {"codigo": str(code)},
        http_get=http_get,
    )
    assert rows == []
    assert http_get.calls == []


def test_fetch_resultado_pages_for_codes_pauses_between_codes() -> None:
    class FakeSleep:
        def __init__(self) -> None:
            self.calls: list[float] = []

        def __call__(self, seconds: float) -> None:
            self.calls.append(seconds)

    sleep = FakeSleep()
    http_get = FakeHttpGetByCodigo(
        {
            "10": {
                "resultado": [{"idCompra": 1}],
                "totalPaginas": 1,
                "paginasRestantes": 0,
            },
            "20": {
                "resultado": [{"idCompra": 2}],
                "totalPaginas": 1,
                "paginasRestantes": 0,
            },
        }
    )
    rows = fetch_resultado_pages_for_codes(
        "https://example.test/preco",
        {"Authorization": "key"},
        codes=[10, 20],
        params_for_code=lambda code: {"codigo": str(code)},
        http_get=http_get,
        pause_seconds=1.0,
        sleep_fn=sleep,
    )
    assert rows == [{"idCompra": 1}, {"idCompra": 2}]
    assert sleep.calls == [1.0]

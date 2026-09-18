from typing import Any

from clients.compras_api import fetch_all_resultado_pages


class FakeResponse:
    def __init__(self, payload: dict[str, Any], status_code: int = 200) -> None:
        self._payload = payload
        self.status_code = status_code

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            raise RuntimeError(f"http error status={self.status_code}")

    def json(self) -> dict[str, Any]:
        return self._payload


class FakeHttpGet:
    """Named fake that returns canned pages by `pagina` query param."""

    def __init__(self, pages: dict[int, dict[str, Any]]) -> None:
        self._pages = pages
        self.calls: list[dict[str, Any]] = []

    def __call__(
        self,
        url: str,
        *,
        headers: dict[str, str],
        params: dict[str, int],
        timeout: int,
    ) -> FakeResponse:
        self.calls.append({"url": url, "headers": headers, "params": params, "timeout": timeout})
        return FakeResponse(self._pages[params["pagina"]])


def test_fetch_all_resultado_pages_walks_every_page() -> None:
    http_get = FakeHttpGet(
        {
            1: {
                "resultado": [{"codigoPdm": 1}],
                "totalPaginas": 2,
                "paginasRestantes": 1,
            },
            2: {
                "resultado": [{"codigoPdm": 2}],
                "totalPaginas": 2,
                "paginasRestantes": 0,
            },
        }
    )
    rows = fetch_all_resultado_pages(
        "https://example.test/pdm",
        {"Authorization": "key"},
        page_size=10,
        http_get=http_get,
    )
    assert rows == [{"codigoPdm": 1}, {"codigoPdm": 2}]
    assert [call["params"]["pagina"] for call in http_get.calls] == [1, 2]
    assert all(call["params"]["tamanhoPagina"] == 10 for call in http_get.calls)


def test_fetch_all_resultado_pages_omits_tamanho_pagina_when_unset() -> None:
    http_get = FakeHttpGet(
        {
            1: {
                "resultado": [{"codigoClasse": 1}],
                "totalPaginas": 1,
                "paginasRestantes": 0,
            },
        }
    )
    rows = fetch_all_resultado_pages(
        "https://example.test/classe",
        {"Authorization": "key"},
        page_size=None,
        http_get=http_get,
    )
    assert rows == [{"codigoClasse": 1}]
    assert http_get.calls[0]["params"] == {"pagina": 1}

from typing import Any

import pytest

from clients.compras_api import fetch_all_resultado_pages, fetch_one_resultado_page


class FakeResponse:
    def __init__(
        self,
        payload: dict[str, Any],
        status_code: int = 200,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._payload = payload
        self.status_code = status_code
        self.headers = headers if headers is not None else {}

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
        params: dict[str, str | int | bool],
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


def test_fetch_one_resultado_page_returns_rows_and_total() -> None:
    http_get = FakeHttpGet(
        {
            2: {
                "resultado": [{"codigoPdm": 9}],
                "totalPaginas": 4,
                "paginasRestantes": 2,
            },
        }
    )
    rows, total_paginas = fetch_one_resultado_page(
        "https://example.test/pdm",
        {"Authorization": "key"},
        pagina=2,
        page_size=10,
        http_get=http_get,
    )
    assert rows == [{"codigoPdm": 9}]
    assert total_paginas == 4
    assert http_get.calls[0]["params"] == {"pagina": 2, "tamanhoPagina": 10}


def test_fetch_one_resultado_page_returns_rows_and_total() -> None:
    http_get = FakeHttpGet(
        {
            2: {
                "resultado": [{"codigoPdm": 9}],
                "totalPaginas": 4,
                "paginasRestantes": 2,
            },
        }
    )
    rows, total_paginas = fetch_one_resultado_page(
        "https://example.test/pdm",
        {"Authorization": "key"},
        pagina=2,
        page_size=10,
        http_get=http_get,
    )
    assert rows == [{"codigoPdm": 9}]
    assert total_paginas == 4
    assert http_get.calls[0]["params"] == {"pagina": 2, "tamanhoPagina": 10}


def test_fetch_all_resultado_pages_sends_query_params() -> None:
    http_get = FakeHttpGet(
        {
            1: {
                "resultado": [{"idCompra": 1}],
                "totalPaginas": 1,
                "paginasRestantes": 0,
            },
        }
    )
    rows = fetch_all_resultado_pages(
        "https://example.test/preco",
        {"Authorization": "key"},
        page_size=20,
        query_params={"tipo": "codigoItemCatalogo", "codigo": "123"},
        http_get=http_get,
    )
    assert rows == [{"idCompra": 1}]
    assert http_get.calls[0]["params"] == {
        "pagina": 1,
        "tamanhoPagina": 20,
        "tipo": "codigoItemCatalogo",
        "codigo": "123",
    }


def test_fetch_all_resultado_pages_treats_zero_total_paginas_as_empty() -> None:
    http_get = FakeHttpGet(
        {
            1: {
                "resultado": [],
                "totalPaginas": 0,
                "paginasRestantes": 0,
            },
        }
    )
    rows = fetch_all_resultado_pages(
        "https://example.test/preco",
        {"Authorization": "key"},
        page_size=20,
        query_params={"tipo": "codigoItemCatalogo", "codigo": "1"},
        http_get=http_get,
    )
    assert rows == []
    assert len(http_get.calls) == 1


class FakeSleep:
    def __init__(self) -> None:
        self.calls: list[float] = []

    def __call__(self, seconds: float) -> None:
        self.calls.append(seconds)


class FakeHttpGetSequence:
    """Named fake that returns canned responses in call order."""

    def __init__(self, responses: list[FakeResponse]) -> None:
        self._responses = list(responses)
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
        if not self._responses:
            raise AssertionError("unexpected extra HTTP call")
        return self._responses.pop(0)


def _ok_page() -> dict[str, Any]:
    return {"resultado": [{"idCompra": 1}], "totalPaginas": 1, "paginasRestantes": 0}


def test_fetch_all_resultado_pages_retries_429_then_succeeds() -> None:
    sleep = FakeSleep()
    http_get = FakeHttpGetSequence(
        [
            FakeResponse({}, status_code=429, headers={"Retry-After": "2"}),
            FakeResponse(_ok_page()),
        ]
    )
    rows = fetch_all_resultado_pages(
        "https://example.test/preco",
        {"Authorization": "key"},
        page_size=20,
        http_get=http_get,
        sleep_fn=sleep,
        max_retries=2,
    )
    assert rows == [{"idCompra": 1}]
    assert len(http_get.calls) == 2
    assert sleep.calls == [2.0]


def test_fetch_all_resultado_pages_raises_after_retrying_429() -> None:
    sleep = FakeSleep()
    http_get = FakeHttpGetSequence(
        [
            FakeResponse({}, status_code=429),
            FakeResponse({}, status_code=429),
        ]
    )
    with pytest.raises(RuntimeError, match="http error status=429"):
        fetch_all_resultado_pages(
            "https://example.test/preco",
            {"Authorization": "key"},
            page_size=20,
            http_get=http_get,
            sleep_fn=sleep,
            max_retries=1,
        )
    assert len(http_get.calls) == 2
    assert sleep.calls == [1.0]


def test_fetch_all_resultado_pages_retries_connection_error() -> None:
    from requests.exceptions import ConnectionError as RequestsConnectionError

    sleep = FakeSleep()
    ok = FakeResponse(_ok_page())

    class FakeHttpGetConnectionThenOk:
        def __init__(self) -> None:
            self.calls = 0

        def __call__(
            self,
            url: str,
            *,
            headers: dict[str, str],
            params: dict[str, str | int | bool],
            timeout: int,
        ) -> FakeResponse:
            self.calls += 1
            if self.calls == 1:
                raise RequestsConnectionError("network is unreachable")
            return ok

    http_get = FakeHttpGetConnectionThenOk()
    rows = fetch_all_resultado_pages(
        "https://example.test/preco",
        {"Authorization": "key"},
        page_size=20,
        http_get=http_get,
        sleep_fn=sleep,
        max_retries=2,
    )
    assert rows == [{"idCompra": 1}]
    assert http_get.calls == 2
    assert sleep.calls == [1.0]

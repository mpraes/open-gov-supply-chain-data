from typing import Any

from clients.compras_api import fetch_one_json_array_page, fetch_one_releases_page


class FakeJsonResponse:
    def __init__(self, payload: object) -> None:
        self._payload = payload
        self.status_code = 200
        self.headers: dict[str, str] = {}

    def raise_for_status(self) -> None:
        return None

    def json(self) -> object:
        return self._payload


def test_fetch_one_releases_page_continues_when_next_link_exists() -> None:
    payload = {
        "releases": [{"ocid": "a", "id": "1"}],
        "links": {"next": "https://example/next"},
    }

    def http_get(url: str, **kwargs: Any) -> FakeJsonResponse:
        assert kwargs["params"]["page"] == 1
        assert kwargs["params"]["offSet"] == 10
        return FakeJsonResponse(payload)

    rows, total = fetch_one_releases_page(
        "https://api/ocds",
        {"Authorization": "x"},
        pagina=1,
        page_size=10,
        http_get=http_get,
        query_params={"buyerID": "1"},
    )
    assert rows[0]["ocid"] == "a"
    assert total == 2


def test_fetch_one_json_array_page_is_single_page() -> None:
    def http_get(url: str, **kwargs: Any) -> FakeJsonResponse:
        return FakeJsonResponse([{"ticketAnalise": "t-1"}])

    rows, total = fetch_one_json_array_page(
        "https://api/alice",
        {"Authorization": "x"},
        pagina=1,
        http_get=http_get,
    )
    assert rows == [{"ticketAnalise": "t-1"}]
    assert total == 1
    later, later_total = fetch_one_json_array_page(
        "https://api/alice",
        {"Authorization": "x"},
        pagina=2,
        http_get=http_get,
    )
    assert later == []
    assert later_total == 1

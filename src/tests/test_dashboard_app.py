from fakes.analytics_db import FakeAnalyticsConnection

from dashboard.app import create_app
from fastapi.testclient import TestClient


class FakeConnectFactory:
    def __init__(self, conn: FakeAnalyticsConnection) -> None:
        self.conn = conn
        self.calls = 0

    def __call__(self) -> FakeAnalyticsConnection:
        self.calls += 1
        return self.conn


class BoomConnectFactory:
    def __call__(self) -> FakeAnalyticsConnection:
        raise RuntimeError("postgres down")


def _overview_sets() -> list[list[tuple[object, ...]]]:
    return [
        [(1,)],
        [(2,)],
        [(3,)],
        [(4,)],
        [(0,)],
        [(0,)],
        [],
        [],
    ]


def test_api_overview_200_with_empty_lists() -> None:
    factory = FakeConnectFactory(FakeAnalyticsConnection(_overview_sets()))
    client = TestClient(create_app(connect_factory=factory))
    response = client.get("/api/kpis/overview")
    assert response.status_code == 200
    body = response.json()
    assert body["ranked_left"] == []
    assert body["leaderboard_left"] == []
    assert factory.conn.closed is True


def test_api_invalid_timeframe_400() -> None:
    factory = FakeConnectFactory(FakeAnalyticsConnection([]))
    client = TestClient(create_app(connect_factory=factory))
    response = client.get("/api/kpis/overview", params={"timeframe": "year"})
    assert response.status_code == 400
    assert "year" in response.text


def test_api_connect_failure_503() -> None:
    client = TestClient(create_app(connect_factory=BoomConnectFactory()))
    response = client.get("/api/kpis/overview")
    assert response.status_code == 503
    body = response.json()
    assert body["error"] == "analytics_unavailable"
    assert "postgres down" in body["detail"]


def test_page_routes_render() -> None:
    factory = FakeConnectFactory(FakeAnalyticsConnection([]))
    client = TestClient(create_app(connect_factory=factory))
    for path in ("/", "/fornecedor", "/material", "/servico", "/uasg"):
        response = client.get(path)
        assert response.status_code == 200
        assert "text/html" in response.headers["content-type"]

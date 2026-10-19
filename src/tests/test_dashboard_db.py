from dashboard.db import connect_analytics
from dashboard.settings import DashboardSettings


class FakeAnalyticsConnect:
    """Falso que grava os kwargs de connect e devolve uma conexão sentinela."""

    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []
        self.connection = object()

    def __call__(
        self,
        *,
        host: str,
        port: str,
        user: str,
        password: str,
        dbname: str,
        options: str,
    ) -> object:
        self.calls.append(
            {
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "dbname": dbname,
                "options": options,
            }
        )
        return self.connection


def test_connect_analytics_sets_analytics_search_path() -> None:
    fake = FakeAnalyticsConnect()
    settings = DashboardSettings(
        host="h", port="5432", user="u", password="p", dbname="d"
    )
    conn = connect_analytics(settings, connect_fn=fake)
    assert conn is fake.connection
    assert fake.calls == [
        {
            "host": "h",
            "port": "5432",
            "user": "u",
            "password": "p",
            "dbname": "d",
            "options": "-c search_path=analytics -c statement_timeout=180s",
        }
    ]

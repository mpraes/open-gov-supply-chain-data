from collections.abc import Callable
from typing import Protocol

from psycopg2 import connect as psycopg2_connect

from dashboard.settings import DashboardSettings


class AnalyticsCursor(Protocol):
    def execute(self, query: str, params: tuple[object, ...] | None = None) -> None: ...
    def fetchone(self) -> tuple[object, ...] | None: ...
    def fetchall(self) -> list[tuple[object, ...]]: ...


class AnalyticsConnection(Protocol):
    def cursor(self) -> AnalyticsCursor: ...
    def close(self) -> None: ...


ConnectFn = Callable[..., AnalyticsConnection]


def connect_analytics(
    settings: DashboardSettings,
    *,
    connect_fn: ConnectFn = psycopg2_connect,
) -> AnalyticsConnection:
    return connect_fn(
        host=settings.host,
        port=settings.port,
        user=settings.user,
        password=settings.password,
        dbname=settings.dbname,
        options="-c search_path=analytics",
    )

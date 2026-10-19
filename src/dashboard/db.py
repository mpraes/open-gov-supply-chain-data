"""Conexão psycopg2 com search_path no schema analytics."""

from collections.abc import Callable
from typing import Protocol

from psycopg2 import connect as psycopg2_connect

from dashboard.settings import DashboardSettings


class AnalyticsCursor(Protocol):
    """Cursor de leitura do schema analytics."""

    def execute(self, query: str, params: tuple[object, ...] | None = None) -> None:
        """Executa a consulta no cursor de analytics."""
        ...

    def fetchone(self) -> tuple[object, ...] | None:
        """Devolve a próxima linha do cursor, ou None quando não há mais linhas."""
        ...

    def fetchall(self) -> list[tuple[object, ...]]:
        """Devolve todas as linhas restantes do cursor."""
        ...


class AnalyticsConnection(Protocol):
    """Conexão que abre um cursor de analytics e pode ser fechada."""

    def cursor(self) -> AnalyticsCursor:
        """Abre um cursor para consultas no schema analytics."""
        ...

    def close(self) -> None:
        """Fecha a conexão com o Postgres de analytics."""
        ...


ConnectFn = Callable[..., AnalyticsConnection]


def connect_analytics(
    settings: DashboardSettings,
    *,
    connect_fn: ConnectFn = psycopg2_connect,
) -> AnalyticsConnection:
    """Abre o Postgres com search_path=analytics e statement_timeout de 180s."""
    return connect_fn(
        host=settings.host,
        port=settings.port,
        user=settings.user,
        password=settings.password,
        dbname=settings.dbname,
        options="-c search_path=analytics -c statement_timeout=180s",
    )

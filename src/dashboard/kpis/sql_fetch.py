"""Executa consultas de leitura no cursor de analytics."""

from dashboard.db import AnalyticsConnection


def fetch_one_row(conn: AnalyticsConnection, query: str) -> tuple[object, ...] | None:
    """Executa a consulta e devolve a primeira linha, ou None."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchone()


def fetch_rows(conn: AnalyticsConnection, query: str) -> list[tuple[object, ...]]:
    """Executa a consulta e devolve todas as linhas."""
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

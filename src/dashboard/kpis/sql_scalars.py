"""Converte linhas de analytics em inteiros e floats dos KPIs."""

from dashboard.db import AnalyticsConnection
from dashboard.kpis.sql_fetch import fetch_one_row


def four_ints(row: tuple[object, ...] | None) -> tuple[int, int, int, int]:
    """Converte as quatro primeiras colunas em inteiros, ou devolve zeros quando a linha é None.

    Exemplo:
        four_ints(None) == (0, 0, 0, 0)
    """
    if row is None:
        return (0, 0, 0, 0)
    return (int(row[0]), int(row[1]), int(row[2]), int(row[3]))


def scalar_float(conn: AnalyticsConnection, query: str) -> float:
    """Devolve o primeiro valor da consulta como float, ou 0.0 quando não há linha."""
    row = fetch_one_row(conn, query)
    return float(row[0]) if row else 0.0


def scalar_int(conn: AnalyticsConnection, query: str) -> int:
    """Devolve o primeiro valor da consulta como int, ou 0 quando não há linha."""
    row = fetch_one_row(conn, query)
    return int(row[0]) if row else 0

"""KPIs do tema UASG a partir dos rollups de analytics."""

from dashboard.db import AnalyticsConnection
from dashboard.kpis.format_values import (
    brl_leaderboard,
    format_brl,
    format_count,
    ranked_with_pct,
)
from dashboard.kpis.sql_fetch import fetch_one_row, fetch_rows
from dashboard.kpis.rollup_sql import (
    monthly_both_origens_sql,
    sum_both_origens_sql,
    top_spend_sql,
)
from dashboard.kpis.sql_scalars import scalar_float
from dashboard.kpis.timeframe import mes_predicate
from dashboard.kpis.types import (
    KpiCard,
    NamedSeries,
    SeriesPoint,
    ThemeKpis,
    Timeframe,
)

_UF_SQL = "SELECT label, n FROM analytics.kpi_uasg_uf ORDER BY 2 DESC LIMIT 8"


def load_uasg_kpis(conn: AnalyticsConnection, timeframe: Timeframe) -> ThemeKpis:
    """Monta cards, série mensal, rankings de UF e SISG e líderes de gasto de UASG e órgão."""
    pred = mes_predicate(timeframe)
    uasgs, ativas, sisg, siasg, orgaos = _catalog_counts(conn)
    spend = scalar_float(conn, sum_both_origens_sql(pred))
    return ThemeKpis(
        _uasg_cards(uasgs, ativas, sisg, siasg, orgaos, spend),
        (_monthly(conn, pred),),
        ranked_with_pct(_label_amounts(conn, _UF_SQL)),
        ranked_with_pct(_sisg_rank_rows(sisg, uasgs)),
        brl_leaderboard(fetch_rows(conn, top_spend_sql("uasg", timeframe))),
        brl_leaderboard(fetch_rows(conn, top_spend_sql("orgao", timeframe))),
    )


def _catalog_counts(conn: AnalyticsConnection) -> tuple[int, int, int, int, int]:
    """Lê total, ativas, sisg, siasg e orgaos de analytics.kpi_catalog_uasg, ou zeros sem linha."""
    row = fetch_one_row(
        conn,
        "SELECT total, ativas, sisg, siasg, orgaos "
        "FROM analytics.kpi_catalog_uasg",
    )
    if row is None:
        return (0, 0, 0, 0, 0)
    return (int(row[0]), int(row[1]), int(row[2]), int(row[3]), int(row[4]))


def _uasg_cards(
    uasgs: int,
    ativas: int,
    sisg: int,
    siasg: int,
    orgaos: int,
    spend: float,
) -> tuple[KpiCard, ...]:
    """Monta os seis cards de cadastro SISG/SIASG e valor homologado."""
    return (
        KpiCard("UASGs", format_count(uasgs), "Cadastro"),
        KpiCard("Ativas", format_count(ativas), "Status"),
        KpiCard("Uso SISG", format_count(sisg), "Sistema"),
        KpiCard("Adesão SIASG", format_count(siasg), "Sistema"),
        KpiCard("Órgãos", format_count(orgaos), "codigo_orgao"),
        KpiCard("Valor homologado", format_brl(spend), "Compras"),
    )


def _sisg_rank_rows(sisg: int, uasgs: int) -> list[tuple[str, float]]:
    """Monta as barras SISG e Fora do SISG a partir das contagens do catálogo."""
    return [("SISG", float(sisg)), ("Fora do SISG", float(uasgs - sisg))]


def _monthly(conn: AnalyticsConnection, pred: str) -> NamedSeries:
    """Monta a série mensal de valor_total das duas origens no predicado pred."""
    rows = fetch_rows(conn, monthly_both_origens_sql(pred))
    return NamedSeries(
        "Compras", tuple(SeriesPoint(str(p), float(v)) for p, v in rows)
    )


def _label_amounts(
    conn: AnalyticsConnection, query: str
) -> list[tuple[str, float]]:
    """Converte as linhas (rótulo, valor) da consulta em pares de texto e float."""
    return [(str(label), float(amount)) for label, amount in fetch_rows(conn, query)]



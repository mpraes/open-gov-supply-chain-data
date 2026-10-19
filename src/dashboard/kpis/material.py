"""KPIs do tema material a partir dos rollups de analytics."""

from dashboard.db import AnalyticsConnection
from dashboard.kpis.format_values import (
    brl_leaderboard,
    format_brl,
    format_count,
    ranked_with_pct,
)
from dashboard.kpis.sql_fetch import fetch_one_row, fetch_rows
from dashboard.kpis.rollup_sql import (
    monthly_origem_sql,
    priced_count_sql,
    sum_origem_sql,
    top_spend_sql,
)
from dashboard.kpis.sql_scalars import four_ints, scalar_float, scalar_int
from dashboard.kpis.timeframe import mes_predicate
from dashboard.kpis.types import (
    KpiCard,
    NamedSeries,
    SeriesPoint,
    ThemeKpis,
    Timeframe,
)


def load_material_kpis(conn: AnalyticsConnection, timeframe: Timeframe) -> ThemeKpis:
    """Monta cards, série mensal, rankings de grupo e líderes de gasto da origem material."""
    pred = mes_predicate(timeframe)
    itens, ativos, sustentaveis, margem = _catalog_counts(conn)
    spend = scalar_float(conn, sum_origem_sql("material", pred))
    priced = scalar_int(conn, priced_count_sql("n_item_material", timeframe))
    return ThemeKpis(
        _material_cards(itens, ativos, sustentaveis, margem, spend, priced),
        (_monthly(conn, pred),),
        ranked_with_pct(_label_amounts(conn, _GRUPO_COUNT_SQL)),
        ranked_with_pct(_label_amounts(conn, _grupo_spend_sql(pred)), formatter=format_brl),
        brl_leaderboard(fetch_rows(conn, top_spend_sql("item_material", timeframe))),
        brl_leaderboard(
            fetch_rows(conn, top_spend_sql("fornecedor", timeframe, origem="material"))
        ),
    )


def _catalog_counts(conn: AnalyticsConnection) -> tuple[int, int, int, int]:
    """Lê total, ativos, sustentaveis e margem de analytics.kpi_catalog_material."""
    row = fetch_one_row(
        conn,
        "SELECT total, ativos, sustentaveis, margem "
        "FROM analytics.kpi_catalog_material",
    )
    return four_ints(row)


def _material_cards(
    itens: int,
    ativos: int,
    sustentaveis: int,
    margem: int,
    spend: float,
    priced: int,
) -> tuple[KpiCard, ...]:
    """Monta os seis cards de CATMAT, sustentabilidade e valor homologado."""
    return (
        KpiCard("Itens", format_count(itens), "CATMAT"),
        KpiCard("Ativos", format_count(ativos), "Status"),
        KpiCard("Sustentáveis", format_count(sustentaveis), "Catálogo"),
        KpiCard("Margem preferência", format_count(margem), "Itens"),
        KpiCard("Valor homologado", format_brl(spend), "Preços"),
        KpiCard("Itens com preço", format_count(priced), "Nas fatos"),
    )


def _monthly(conn: AnalyticsConnection, pred: str) -> NamedSeries:
    """Monta a série mensal de valor_total da origem material no predicado pred."""
    rows = fetch_rows(conn, monthly_origem_sql("material", pred))
    return NamedSeries(
        "Material", tuple(SeriesPoint(str(p), float(v)) for p, v in rows)
    )


_GRUPO_COUNT_SQL = (
    "SELECT label, n FROM analytics.kpi_material_grupo_count "
    "ORDER BY 2 DESC LIMIT 8"
)


def _grupo_spend_sql(pred: str) -> str:
    """Monta o SQL dos oito grupos com maior SUM(valor_total) em kpi_mes_grupo_material."""
    return (
        "SELECT nome_grupo, SUM(valor_total) "
        "FROM analytics.kpi_mes_grupo_material "
        f"WHERE {pred} GROUP BY 1 ORDER BY 2 DESC LIMIT 8"
    )


def _label_amounts(conn: AnalyticsConnection, query: str) -> list[tuple[str, float]]:
    """Converte as linhas (rótulo, valor) da consulta em pares de texto e float."""
    return [(str(label), float(amount)) for label, amount in fetch_rows(conn, query)]



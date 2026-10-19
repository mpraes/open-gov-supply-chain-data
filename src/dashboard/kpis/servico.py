"""KPIs do tema serviço a partir dos rollups de analytics."""

from dashboard.db import AnalyticsConnection
from dashboard.kpis.format_values import (
    brl_leaderboard,
    format_brl,
    format_count,
    format_pct,
    ranked_with_pct,
)
from dashboard.kpis.sql_fetch import fetch_one_row, fetch_rows
from dashboard.kpis.rollup_sql import (
    monthly_origem_sql,
    priced_count_sql,
    sum_origem_sql,
    top_spend_sql,
)
from dashboard.kpis.sql_scalars import scalar_float, scalar_int
from dashboard.kpis.timeframe import mes_predicate
from dashboard.kpis.types import (
    KpiCard,
    NamedSeries,
    SeriesPoint,
    ThemeKpis,
    Timeframe,
)


def load_servico_kpis(conn: AnalyticsConnection, timeframe: Timeframe) -> ThemeKpis:
    """Monta cards, série mensal, rankings de seção e grupo e líderes de gasto da origem servico."""
    pred = mes_predicate(timeframe)
    servicos, ativos, exclusivo, ratio = _catalog_counts(conn)
    spend = scalar_float(conn, sum_origem_sql("servico", pred))
    priced = scalar_int(conn, priced_count_sql("n_item_servico", timeframe))
    return ThemeKpis(
        _servico_cards(servicos, ativos, exclusivo, ratio, spend, priced),
        (_monthly(conn, pred),),
        ranked_with_pct(_label_amounts(conn, _SECAO_SQL)),
        ranked_with_pct(_label_amounts(conn, _grupo_spend_sql(pred)), formatter=format_brl),
        brl_leaderboard(fetch_rows(conn, top_spend_sql("item_servico", timeframe))),
        brl_leaderboard(
            fetch_rows(conn, top_spend_sql("fornecedor", timeframe, origem="servico"))
        ),
    )


def _catalog_counts(conn: AnalyticsConnection) -> tuple[int, int, int, float]:
    """Lê total, ativos, exclusivo e cobertura de analytics.kpi_catalog_servico, ou zeros sem linha."""
    row = fetch_one_row(
        conn,
        "SELECT total, ativos, exclusivo, cobertura "
        "FROM analytics.kpi_catalog_servico",
    )
    if row is None:
        return (0, 0, 0, 0.0)
    return (int(row[0]), int(row[1]), int(row[2]), float(row[3]))


def _servico_cards(
    servicos: int,
    ativos: int,
    exclusivo: int,
    ratio: float,
    spend: float,
    priced: int,
) -> tuple[KpiCard, ...]:
    """Monta os seis cards de CATSER, cobertura de hierarquia e valor homologado."""
    return (
        KpiCard("Serviços", format_count(servicos), "CATSER"),
        KpiCard("Ativos", format_count(ativos), "Status"),
        KpiCard("Cobertura hierarquia", format_pct(ratio), "Join subclasse"),
        KpiCard("Valor homologado", format_brl(spend), "Preços"),
        KpiCard("Serviços com preço", format_count(priced), "Nas fatos"),
        KpiCard("Exclusivo central", format_count(exclusivo), "Central de compras"),
    )


def _monthly(conn: AnalyticsConnection, pred: str) -> NamedSeries:
    """Monta a série mensal de valor_total da origem servico no predicado pred."""
    rows = fetch_rows(conn, monthly_origem_sql("servico", pred))
    return NamedSeries(
        "Serviço", tuple(SeriesPoint(str(p), float(v)) for p, v in rows)
    )


_SECAO_SQL = (
    "SELECT label, n FROM analytics.kpi_servico_secao ORDER BY 2 DESC LIMIT 8"
)


def _grupo_spend_sql(pred: str) -> str:
    """Monta o SQL dos oito grupos com maior SUM(valor_total) em kpi_mes_grupo_servico."""
    return (
        "SELECT nome_grupo, SUM(valor_total) "
        "FROM analytics.kpi_mes_grupo_servico "
        f"WHERE {pred} GROUP BY 1 ORDER BY 2 DESC LIMIT 8"
    )


def _label_amounts(
    conn: AnalyticsConnection, query: str
) -> list[tuple[str, float]]:
    """Converte as linhas (rótulo, valor) da consulta em pares de texto e float."""
    return [(str(label), float(amount)) for label, amount in fetch_rows(conn, query)]


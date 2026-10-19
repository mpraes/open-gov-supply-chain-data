"""KPIs da visão geral de catálogo e valores homologados."""

from dashboard.db import AnalyticsConnection
from dashboard.kpis.format_values import format_brl, format_count
from dashboard.kpis.sql_fetch import fetch_one_row, fetch_rows
from dashboard.kpis.rollup_sql import monthly_origem_sql, sum_origem_sql
from dashboard.kpis.sql_scalars import four_ints, scalar_float
from dashboard.kpis.timeframe import mes_predicate
from dashboard.kpis.types import (
    KpiCard,
    NamedSeries,
    SeriesPoint,
    ThemeKpis,
    Timeframe,
)


def load_overview_kpis(conn: AnalyticsConnection, timeframe: Timeframe) -> ThemeKpis:
    """Monta cards de catálogo e séries mensais de valor de material e servico."""
    pred = mes_predicate(timeframe)
    counts = _catalog_counts(conn)
    material_sum = scalar_float(conn, sum_origem_sql("material", pred))
    servico_sum = scalar_float(conn, sum_origem_sql("servico", pred))
    cards = (
        KpiCard("Fornecedores", format_count(counts[0]), "Cadastro"),
        KpiCard("Materiais", format_count(counts[1]), "CATMAT"),
        KpiCard("Serviços", format_count(counts[2]), "CATSER"),
        KpiCard("UASGs", format_count(counts[3]), "Compradoras"),
        KpiCard("Valor material", format_brl(material_sum), "Homologado"),
        KpiCard("Valor serviço", format_brl(servico_sum), "Homologado"),
    )
    series = (
        _monthly_series(conn, "material", pred, "Material"),
        _monthly_series(conn, "servico", pred, "Serviço"),
    )
    return ThemeKpis(cards, series, (), (), (), ())


def _catalog_counts(conn: AnalyticsConnection) -> tuple[int, int, int, int]:
    """Lê fornecedores, materiais, servicos e uasgs de analytics.kpi_catalog_overview."""
    return four_ints(
        fetch_one_row(
            conn,
            "SELECT fornecedores, materiais, servicos, uasgs "
            "FROM analytics.kpi_catalog_overview",
        )
    )


def _monthly_series(
    conn: AnalyticsConnection, origem: str, pred: str, name: str
) -> NamedSeries:
    """Monta a série mensal de valor_total da origem no predicado pred."""
    rows = fetch_rows(conn, monthly_origem_sql(origem, pred))
    points = tuple(SeriesPoint(str(period), float(value)) for period, value in rows)
    return NamedSeries(name, points)

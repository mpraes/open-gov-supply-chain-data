from dashboard.db import AnalyticsConnection
from dashboard.kpis.format_values import format_brl, format_count
from dashboard.kpis.sql_fetch import fetch_one_row, fetch_rows
from dashboard.kpis.timeframe import fact_predicate
from dashboard.kpis.types import (
    KpiCard,
    NamedSeries,
    SeriesPoint,
    ThemeKpis,
    Timeframe,
)


def load_overview_kpis(conn: AnalyticsConnection, timeframe: Timeframe) -> ThemeKpis:
    pred = fact_predicate(timeframe)
    counts = [_count(conn, table) for table in _CATALOG_TABLES]
    material_sum = _sum_fact(conn, "fct_preco_material", pred)
    servico_sum = _sum_fact(conn, "fct_preco_servico", pred)
    cards = (
        KpiCard("Fornecedores", format_count(counts[0]), "Cadastro"),
        KpiCard("Materiais", format_count(counts[1]), "CATMAT"),
        KpiCard("Serviços", format_count(counts[2]), "CATSER"),
        KpiCard("UASGs", format_count(counts[3]), "Compradoras"),
        KpiCard("Valor material", format_brl(material_sum), "Homologado"),
        KpiCard("Valor serviço", format_brl(servico_sum), "Homologado"),
    )
    series = (
        _monthly_series(conn, "fct_preco_material", pred, "Material"),
        _monthly_series(conn, "fct_preco_servico", pred, "Serviço"),
    )
    return ThemeKpis(cards, series, (), (), (), ())


_CATALOG_TABLES = (
    "dim_fornecedor",
    "dim_material_item",
    "dim_servico_item",
    "dim_uasg",
)


def _count(conn: AnalyticsConnection, table: str) -> int:
    row = fetch_one_row(conn, f"SELECT COUNT(*) FROM analytics.{table}")
    return int(row[0]) if row else 0


def _sum_fact(conn: AnalyticsConnection, table: str, pred: str) -> float:
    row = fetch_one_row(
        conn,
        f"SELECT COALESCE(SUM(valor_total_homologado), 0) "
        f"FROM analytics.{table} WHERE {pred}",
    )
    return float(row[0]) if row else 0.0


def _monthly_series(
    conn: AnalyticsConnection, table: str, pred: str, name: str
) -> NamedSeries:
    rows = fetch_rows(
        conn,
        "SELECT to_char(date_trunc('month', data_compra), 'YYYY-MM'), "
        f"COALESCE(SUM(valor_total_homologado), 0) FROM analytics.{table} "
        f"WHERE {pred} AND data_compra IS NOT NULL GROUP BY 1 ORDER BY 1",
    )
    points = tuple(SeriesPoint(str(period), float(value)) for period, value in rows)
    return NamedSeries(name, points)

"""KPIs do tema fornecedor a partir dos rollups de analytics."""

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
    sum_both_origens_sql,
    top_spend_sql,
)
from dashboard.kpis.sql_scalars import four_ints, scalar_float, scalar_int
from dashboard.kpis.timeframe import mes_predicate
from dashboard.kpis.types import (
    KpiCard,
    LeaderboardRow,
    NamedSeries,
    SeriesPoint,
    ThemeKpis,
    Timeframe,
)

_UF_SQL = (
    "SELECT label, n FROM analytics.kpi_fornecedor_uf ORDER BY 2 DESC LIMIT 8"
)
_PORTE_SQL = (
    "SELECT label, n FROM analytics.kpi_fornecedor_porte ORDER BY 2 DESC LIMIT 8"
)


def load_fornecedor_kpis(conn: AnalyticsConnection, timeframe: Timeframe) -> ThemeKpis:
    """Monta cards, séries mensais, rankings de UF e porte e líderes de gasto e CNAE."""
    pred = mes_predicate(timeframe)
    catalog = _catalog_counts(conn)
    spend = scalar_float(conn, sum_both_origens_sql(pred))
    priced = scalar_int(conn, priced_count_sql("n_fornecedor", timeframe))
    return ThemeKpis(
        _fornecedor_cards(*catalog, spend, priced),
        (
            _monthly(conn, "material", pred, "Material"),
            _monthly(conn, "servico", pred, "Serviço"),
        ),
        ranked_with_pct(_label_amounts(conn, _UF_SQL)),
        ranked_with_pct(_label_amounts(conn, _PORTE_SQL)),
        _spend_leaders(conn, timeframe),
        _cnae_leaders(conn),
    )


def _catalog_counts(conn: AnalyticsConnection) -> tuple[int, int, int, int]:
    """Lê total, ativos, habilitados e missing de analytics.kpi_catalog_fornecedor."""
    row = fetch_one_row(
        conn,
        "SELECT total, ativos, habilitados, missing "
        "FROM analytics.kpi_catalog_fornecedor",
    )
    return four_ints(row)


def _fornecedor_cards(
    total: int,
    ativos: int,
    habilitados: int,
    missing: int,
    spend: float,
    distinct_facts: int,
) -> tuple[KpiCard, ...]:
    """Monta os seis cards de cadastro, valor homologado e presença nas fatos."""
    return (
        KpiCard("Fornecedores", format_count(total), "Cadastro"),
        KpiCard("Ativos", format_count(ativos), "Status"),
        KpiCard("Habilitados", format_count(habilitados), "Licitar"),
        KpiCard("Valor homologado", format_brl(spend), "Material + serviço"),
        KpiCard("Nas fatos", format_count(distinct_facts), "Com preço"),
        KpiCard("Não cadastrados", format_count(missing), "Só nas fatos"),
    )


def _monthly(
    conn: AnalyticsConnection, origem: str, pred: str, name: str
) -> NamedSeries:
    """Monta a série mensal de valor_total da origem no predicado pred."""
    rows = fetch_rows(conn, monthly_origem_sql(origem, pred))
    return NamedSeries(
        name, tuple(SeriesPoint(str(period), float(value)) for period, value in rows)
    )


def _label_amounts(conn: AnalyticsConnection, query: str) -> list[tuple[str, float]]:
    """Converte as linhas (rótulo, valor) da consulta em pares de texto e float."""
    return [(str(label), float(amount)) for label, amount in fetch_rows(conn, query)]


def _spend_leaders(
    conn: AnalyticsConnection, timeframe: Timeframe
) -> tuple[LeaderboardRow, ...]:
    """Lê o top de gasto do fornecedor na janela e formata em BRL."""
    return brl_leaderboard(fetch_rows(conn, top_spend_sql("fornecedor", timeframe)))


def _cnae_leaders(conn: AnalyticsConnection) -> tuple[LeaderboardRow, ...]:
    """Lê os oito CNAEs mais frequentes de analytics.kpi_fornecedor_cnae e numera o ranking."""
    rows = fetch_rows(
        conn,
        "SELECT label, n FROM analytics.kpi_fornecedor_cnae "
        "ORDER BY 2 DESC LIMIT 8",
    )
    return tuple(
        LeaderboardRow(str(title), format_count(int(amount)), index)
        for index, (title, amount) in enumerate(rows, start=1)
    )

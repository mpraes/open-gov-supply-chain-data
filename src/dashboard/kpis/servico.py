from dashboard.db import AnalyticsConnection
from dashboard.kpis.format_values import format_brl, format_count, format_pct, ranked_with_pct
from dashboard.kpis.sql_fetch import fetch_one_row, fetch_rows
from dashboard.kpis.rollup_sql import (
    distinct_total_sql,
    monthly_origem_sql,
    spend_leader_sql,
    spend_source,
    sum_origem_sql,
)
from dashboard.kpis.sql_scalars import scalar_float, scalar_int
from dashboard.kpis.timeframe import mes_predicate
from dashboard.kpis.types import (
    KpiCard,
    LeaderboardRow,
    NamedSeries,
    SeriesPoint,
    ThemeKpis,
    Timeframe,
)


def load_servico_kpis(conn: AnalyticsConnection, timeframe: Timeframe) -> ThemeKpis:
    pred = mes_predicate(timeframe)
    servicos, ativos, exclusivo = _catalog_counts(conn)
    ratio = _hierarchy_coverage_ratio(conn)
    spend = scalar_float(conn, sum_origem_sql("servico", pred))
    priced = scalar_int(
        conn, distinct_total_sql("kpi_item_servico_total", "cod_servico", timeframe)
    )
    return ThemeKpis(
        _servico_cards(servicos, ativos, exclusivo, ratio, spend, priced),
        (_monthly(conn, pred),),
        ranked_with_pct(_label_amounts(conn, _SECAO_SQL)),
        ranked_with_pct(_label_amounts(conn, _grupo_spend_sql(pred)), formatter=format_brl),
        _service_leaders(conn, timeframe, pred),
        _supplier_leaders(conn, timeframe, pred),
    )


def _catalog_counts(conn: AnalyticsConnection) -> tuple[int, int, int]:
    row = fetch_one_row(
        conn,
        "SELECT COUNT(*), "
        "COUNT(*) FILTER (WHERE is_ativo), "
        "COUNT(*) FILTER (WHERE is_exclusivo_central_compras) "
        "FROM analytics.dim_servico_item",
    )
    return _three_ints(row)


def _hierarchy_coverage_ratio(conn: AnalyticsConnection) -> float:
    coverage = fetch_one_row(
        conn,
        "SELECT COUNT(*), "
        "COUNT(*) FILTER (WHERE sc.cod_subclasse IS NOT NULL) "
        "FROM analytics.dim_servico_item i "
        "LEFT JOIN analytics.dim_servico_subclasse sc "
        "ON sc.cod_subclasse = i.cod_subclasse",
    )
    if not coverage:
        return 0.0
    total, joined = int(coverage[0]), int(coverage[1])
    return (joined / total) if total else 0.0


def _servico_cards(
    servicos: int,
    ativos: int,
    exclusivo: int,
    ratio: float,
    spend: float,
    priced: int,
) -> tuple[KpiCard, ...]:
    return (
        KpiCard("Serviços", format_count(servicos), "CATSER"),
        KpiCard("Ativos", format_count(ativos), "Status"),
        KpiCard("Cobertura hierarquia", format_pct(ratio), "Join subclasse"),
        KpiCard("Valor homologado", format_brl(spend), "Preços"),
        KpiCard("Serviços com preço", format_count(priced), "Nas fatos"),
        KpiCard("Exclusivo central", format_count(exclusivo), "Central de compras"),
    )


def _monthly(conn: AnalyticsConnection, pred: str) -> NamedSeries:
    rows = fetch_rows(conn, monthly_origem_sql("servico", pred))
    return NamedSeries(
        "Serviço", tuple(SeriesPoint(str(p), float(v)) for p, v in rows)
    )


_SECAO_SQL = (
    "SELECT COALESCE(s.nome_secao, CAST(i.cod_secao AS text)), COUNT(*) "
    "FROM analytics.stg_servico_item i "
    "LEFT JOIN analytics.dim_servico_secao s ON s.cod_secao = i.cod_secao "
    "GROUP BY 1 ORDER BY 2 DESC LIMIT 8"
)


def _grupo_spend_sql(pred: str) -> str:
    return (
        "SELECT nome_grupo, SUM(valor_total) "
        "FROM analytics.kpi_mes_grupo_servico "
        f"WHERE {pred} GROUP BY 1 ORDER BY 2 DESC LIMIT 8"
    )


def _label_amounts(
    conn: AnalyticsConnection, query: str
) -> list[tuple[str, float]]:
    return [(str(label), float(amount)) for label, amount in fetch_rows(conn, query)]


def _service_leaders(
    conn: AnalyticsConnection, timeframe: Timeframe, pred: str
) -> tuple[LeaderboardRow, ...]:
    table = spend_source(timeframe, "kpi_mes_item_servico", "kpi_item_servico_total")
    rows = fetch_rows(
        conn,
        spend_leader_sql(
            table,
            "cod_servico",
            "d.nome_servico",
            "analytics.dim_servico_item",
            pred,
        ),
    )
    return tuple(
        LeaderboardRow(str(title), format_brl(float(amount)), index)
        for index, (title, _key, amount) in enumerate(rows, start=1)
    )


def _supplier_leaders(
    conn: AnalyticsConnection, timeframe: Timeframe, pred: str
) -> tuple[LeaderboardRow, ...]:
    table = spend_source(timeframe, "kpi_mes_fornecedor", "kpi_fornecedor_total")
    rows = fetch_rows(
        conn,
        spend_leader_sql(
            table,
            "ni_fornecedor",
            "d.nome_razao_social",
            "analytics.dim_fornecedor",
            pred,
            extra_pred="origem = 'servico'",
        ),
    )
    return tuple(
        LeaderboardRow(str(title), format_brl(float(amount)), index)
        for index, (title, _ni, amount) in enumerate(rows, start=1)
    )


def _three_ints(row: tuple[object, ...] | None) -> tuple[int, int, int]:
    if row is None:
        return (0, 0, 0)
    return (int(row[0]), int(row[1]), int(row[2]))

from dashboard.db import AnalyticsConnection
from dashboard.kpis.format_values import format_brl, format_count, format_pct, ranked_with_pct
from dashboard.kpis.sql_fetch import fetch_one_row, fetch_rows
from dashboard.kpis.sql_scalars import scalar_float, scalar_int
from dashboard.kpis.timeframe import fact_predicate
from dashboard.kpis.types import (
    KpiCard,
    LeaderboardRow,
    NamedSeries,
    SeriesPoint,
    ThemeKpis,
    Timeframe,
)


def load_servico_kpis(conn: AnalyticsConnection, timeframe: Timeframe) -> ThemeKpis:
    pred = fact_predicate(timeframe)
    servicos, ativos, exclusivo = _catalog_counts(conn)
    ratio = _hierarchy_coverage_ratio(conn)
    spend = _homologado_spend(conn, pred)
    priced = _priced_servico_count(conn, pred)
    return ThemeKpis(
        _servico_cards(servicos, ativos, exclusivo, ratio, spend, priced),
        (_monthly(conn, pred),),
        ranked_with_pct(_label_amounts(conn, _SECAO_SQL)),
        ranked_with_pct(_label_amounts(conn, _grupo_spend_sql(pred))),
        _service_leaders(conn, pred),
        _supplier_leaders(conn, pred),
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


def _homologado_spend(conn: AnalyticsConnection, pred: str) -> float:
    return scalar_float(
        conn,
        "SELECT COALESCE(SUM(valor_total_homologado), 0) "
        f"FROM analytics.fct_preco_servico WHERE {pred}",
    )


def _priced_servico_count(conn: AnalyticsConnection, pred: str) -> int:
    return scalar_int(
        conn,
        "SELECT COUNT(DISTINCT cod_servico) "
        f"FROM analytics.fct_preco_servico WHERE {pred}",
    )


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
    rows = fetch_rows(
        conn,
        "SELECT to_char(date_trunc('month', data_compra), 'YYYY-MM'), "
        "COALESCE(SUM(valor_total_homologado), 0) "
        f"FROM analytics.fct_preco_servico WHERE {pred} "
        "AND data_compra IS NOT NULL GROUP BY 1 ORDER BY 1",
    )
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
        "SELECT COALESCE(g.nome_grupo, CAST(i.cod_grupo AS text)), "
        "SUM(f.valor_total_homologado) FROM analytics.fct_preco_servico f "
        "JOIN analytics.stg_servico_item i ON i.cod_servico = f.cod_servico "
        "LEFT JOIN analytics.dim_servico_grupo g ON g.cod_grupo = i.cod_grupo "
        f"WHERE {pred} GROUP BY 1 ORDER BY 2 DESC LIMIT 8"
    )


def _label_amounts(
    conn: AnalyticsConnection, query: str
) -> list[tuple[str, float]]:
    return [(str(label), float(amount)) for label, amount in fetch_rows(conn, query)]


def _service_leaders(conn: AnalyticsConnection, pred: str) -> tuple[LeaderboardRow, ...]:
    rows = fetch_rows(
        conn,
        "SELECT COALESCE(i.nome_servico, CAST(f.cod_servico AS text)), "
        "SUM(f.valor_total_homologado) FROM analytics.fct_preco_servico f "
        "LEFT JOIN analytics.dim_servico_item i ON i.cod_servico = f.cod_servico "
        f"WHERE {pred} GROUP BY 1 ORDER BY 2 DESC LIMIT 8",
    )
    return tuple(
        LeaderboardRow(str(title), format_brl(float(amount)), index)
        for index, (title, amount) in enumerate(rows, start=1)
    )


def _supplier_leaders(
    conn: AnalyticsConnection, pred: str
) -> tuple[LeaderboardRow, ...]:
    rows = fetch_rows(
        conn,
        "SELECT COALESCE(d.nome_razao_social, f.ni_fornecedor), f.ni_fornecedor, "
        "SUM(f.valor_total_homologado) FROM analytics.fct_preco_servico f "
        "LEFT JOIN analytics.dim_fornecedor d ON d.ni_fornecedor = f.ni_fornecedor "
        f"WHERE {pred} GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 8",
    )
    return tuple(
        LeaderboardRow(str(title), str(subtitle), index)
        for index, (title, subtitle, _amount) in enumerate(rows, start=1)
    )


def _three_ints(row: tuple[object, ...] | None) -> tuple[int, int, int]:
    if row is None:
        return (0, 0, 0)
    return (int(row[0]), int(row[1]), int(row[2]))

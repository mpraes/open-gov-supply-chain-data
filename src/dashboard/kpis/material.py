from dashboard.db import AnalyticsConnection
from dashboard.kpis.format_values import format_brl, format_count, ranked_with_pct
from dashboard.kpis.sql_fetch import fetch_one_row, fetch_rows
from dashboard.kpis.sql_scalars import four_ints, scalar_float, scalar_int
from dashboard.kpis.timeframe import fact_predicate
from dashboard.kpis.types import (
    KpiCard,
    LeaderboardRow,
    NamedSeries,
    SeriesPoint,
    ThemeKpis,
    Timeframe,
)


def load_material_kpis(conn: AnalyticsConnection, timeframe: Timeframe) -> ThemeKpis:
    pred = fact_predicate(timeframe)
    itens, ativos, sustentaveis, margem = _catalog_counts(conn)
    spend = _homologado_spend(conn, pred)
    priced = _priced_item_count(conn, pred)
    return ThemeKpis(
        _material_cards(itens, ativos, sustentaveis, margem, spend, priced),
        (_monthly(conn, pred),),
        ranked_with_pct(_label_amounts(conn, _GRUPO_COUNT_SQL)),
        ranked_with_pct(_label_amounts(conn, _grupo_spend_sql(pred)), formatter=format_brl),
        _item_leaders(conn, pred),
        _supplier_leaders(conn, pred),
    )


def _catalog_counts(conn: AnalyticsConnection) -> tuple[int, int, int, int]:
    row = fetch_one_row(
        conn,
        "SELECT COUNT(*), "
        "COUNT(*) FILTER (WHERE is_ativo), "
        "COUNT(*) FILTER (WHERE is_sustentavel), "
        "COUNT(*) FILTER (WHERE aplica_margem_preferencia) "
        "FROM analytics.dim_material_item",
    )
    return four_ints(row)


def _homologado_spend(conn: AnalyticsConnection, pred: str) -> float:
    return scalar_float(
        conn,
        "SELECT COALESCE(SUM(valor_total_homologado), 0) "
        f"FROM analytics.fct_preco_material WHERE {pred}",
    )


def _priced_item_count(conn: AnalyticsConnection, pred: str) -> int:
    return scalar_int(
        conn,
        "SELECT COUNT(DISTINCT cod_item) "
        f"FROM analytics.fct_preco_material WHERE {pred}",
    )


def _material_cards(
    itens: int,
    ativos: int,
    sustentaveis: int,
    margem: int,
    spend: float,
    priced: int,
) -> tuple[KpiCard, ...]:
    return (
        KpiCard("Itens", format_count(itens), "CATMAT"),
        KpiCard("Ativos", format_count(ativos), "Status"),
        KpiCard("Sustentáveis", format_count(sustentaveis), "Catálogo"),
        KpiCard("Margem preferência", format_count(margem), "Itens"),
        KpiCard("Valor homologado", format_brl(spend), "Preços"),
        KpiCard("Itens com preço", format_count(priced), "Nas fatos"),
    )


def _monthly(conn: AnalyticsConnection, pred: str) -> NamedSeries:
    rows = fetch_rows(
        conn,
        "SELECT to_char(date_trunc('month', data_compra), 'YYYY-MM'), "
        "COALESCE(SUM(valor_total_homologado), 0) "
        f"FROM analytics.fct_preco_material WHERE {pred} "
        "AND data_compra IS NOT NULL GROUP BY 1 ORDER BY 1",
    )
    return NamedSeries(
        "Material", tuple(SeriesPoint(str(p), float(v)) for p, v in rows)
    )


_GRUPO_COUNT_SQL = (
    "SELECT g.nome_grupo, COUNT(*) FROM analytics.dim_material_item i "
    "JOIN analytics.dim_material_pdm p ON p.cod_pdm = i.cod_pdm "
    "JOIN analytics.dim_material_classe c ON c.cod_classe = p.cod_classe "
    "JOIN analytics.dim_material_grupo g ON g.cod_grupo = c.cod_grupo "
    "GROUP BY 1 ORDER BY 2 DESC LIMIT 8"
)


def _grupo_spend_sql(pred: str) -> str:
    return (
        "SELECT g.nome_grupo, SUM(f.valor_total_homologado) "
        "FROM analytics.fct_preco_material f "
        "JOIN analytics.dim_material_item i ON i.cod_item = f.cod_item "
        "JOIN analytics.dim_material_pdm p ON p.cod_pdm = i.cod_pdm "
        "JOIN analytics.dim_material_classe c ON c.cod_classe = p.cod_classe "
        "JOIN analytics.dim_material_grupo g ON g.cod_grupo = c.cod_grupo "
        f"WHERE {pred} GROUP BY 1 ORDER BY 2 DESC LIMIT 8"
    )


def _label_amounts(conn: AnalyticsConnection, query: str) -> list[tuple[str, float]]:
    return [(str(label), float(amount)) for label, amount in fetch_rows(conn, query)]


def _item_leaders(conn: AnalyticsConnection, pred: str) -> tuple[LeaderboardRow, ...]:
    rows = fetch_rows(
        conn,
        "SELECT COALESCE(i.descricao_item, CAST(f.cod_item AS text)), "
        "SUM(f.valor_total_homologado) FROM analytics.fct_preco_material f "
        "LEFT JOIN analytics.dim_material_item i ON i.cod_item = f.cod_item "
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
        "SUM(f.valor_total_homologado) FROM analytics.fct_preco_material f "
        "LEFT JOIN analytics.dim_fornecedor d ON d.ni_fornecedor = f.ni_fornecedor "
        f"WHERE {pred} GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 8",
    )
    return tuple(
        LeaderboardRow(str(title), format_brl(float(amount)), index)
        for index, (title, _ni, amount) in enumerate(rows, start=1)
    )

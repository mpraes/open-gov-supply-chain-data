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

_NOT_REGISTERED = "FORNECEDOR NÃO CADASTRADO NO CADASTRO GERAL"

_UF_SQL = (
    "SELECT COALESCE(sigla_uf, '(sem UF)'), COUNT(*) "
    "FROM analytics.dim_fornecedor GROUP BY 1 ORDER BY 2 DESC LIMIT 8"
)
_PORTE_SQL = (
    "SELECT COALESCE(NULLIF(TRIM(nome_porte_empresa), ''), '(sem porte)'), "
    "COUNT(*) FROM analytics.dim_fornecedor GROUP BY 1 ORDER BY 2 DESC LIMIT 8"
)


def load_fornecedor_kpis(conn: AnalyticsConnection, timeframe: Timeframe) -> ThemeKpis:
    pred = fact_predicate(timeframe)
    total, ativos, habilitados, missing = _catalog_counts(conn)
    spend = _union_homologado_spend(conn, pred)
    distinct_facts = _distinct_ni_in_facts(conn, pred)
    cards = _fornecedor_cards(
        total, ativos, habilitados, missing, spend, distinct_facts
    )
    return ThemeKpis(
        cards,
        (
            _monthly(conn, "fct_preco_material", pred, "Material"),
            _monthly(conn, "fct_preco_servico", pred, "Serviço"),
        ),
        ranked_with_pct(_label_amounts(conn, _UF_SQL)),
        ranked_with_pct(_label_amounts(conn, _PORTE_SQL)),
        _spend_leaders(conn, pred),
        _cnae_leaders(conn),
    )


def _catalog_counts(conn: AnalyticsConnection) -> tuple[int, int, int, int]:
    row = fetch_one_row(
        conn,
        "SELECT COUNT(*), "
        "COUNT(*) FILTER (WHERE is_ativo), "
        "COUNT(*) FILTER (WHERE is_habilitado_licitar), "
        f"COUNT(*) FILTER (WHERE nome_razao_social = '{_NOT_REGISTERED}') "
        "FROM analytics.dim_fornecedor",
    )
    return four_ints(row)


def _union_homologado_spend(conn: AnalyticsConnection, pred: str) -> float:
    return scalar_float(
        conn,
        "SELECT COALESCE(SUM(valor_total_homologado), 0) FROM ("
        f"SELECT valor_total_homologado FROM analytics.fct_preco_material WHERE {pred} "
        "UNION ALL "
        f"SELECT valor_total_homologado FROM analytics.fct_preco_servico WHERE {pred}"
        ") s",
    )


def _distinct_ni_in_facts(conn: AnalyticsConnection, pred: str) -> int:
    return scalar_int(
        conn,
        "SELECT COUNT(DISTINCT ni_fornecedor) FROM ("
        f"SELECT ni_fornecedor FROM analytics.fct_preco_material WHERE {pred} "
        "UNION "
        f"SELECT ni_fornecedor FROM analytics.fct_preco_servico WHERE {pred}"
        ") s",
    )


def _fornecedor_cards(
    total: int,
    ativos: int,
    habilitados: int,
    missing: int,
    spend: float,
    distinct_facts: int,
) -> tuple[KpiCard, ...]:
    return (
        KpiCard("Fornecedores", format_count(total), "Cadastro"),
        KpiCard("Ativos", format_count(ativos), "Status"),
        KpiCard("Habilitados", format_count(habilitados), "Licitar"),
        KpiCard("Valor homologado", format_brl(spend), "Material + serviço"),
        KpiCard("Nas fatos", format_count(distinct_facts), "Com preço"),
        KpiCard("Não cadastrados", format_count(missing), "Só nas fatos"),
    )


def _monthly(
    conn: AnalyticsConnection, table: str, pred: str, name: str
) -> NamedSeries:
    rows = fetch_rows(
        conn,
        "SELECT to_char(date_trunc('month', data_compra), 'YYYY-MM'), "
        f"COALESCE(SUM(valor_total_homologado), 0) FROM analytics.{table} "
        f"WHERE {pred} AND data_compra IS NOT NULL GROUP BY 1 ORDER BY 1",
    )
    return NamedSeries(
        name, tuple(SeriesPoint(str(period), float(value)) for period, value in rows)
    )


def _label_amounts(conn: AnalyticsConnection, query: str) -> list[tuple[str, float]]:
    return [(str(label), float(amount)) for label, amount in fetch_rows(conn, query)]


def _spend_leaders(conn: AnalyticsConnection, pred: str) -> tuple[LeaderboardRow, ...]:
    rows = fetch_rows(
        conn,
        "SELECT COALESCE(d.nome_razao_social, f.ni_fornecedor), f.ni_fornecedor, "
        "SUM(f.valor_total_homologado) FROM ("
        f"SELECT ni_fornecedor, valor_total_homologado FROM analytics.fct_preco_material WHERE {pred} "
        "UNION ALL "
        f"SELECT ni_fornecedor, valor_total_homologado FROM analytics.fct_preco_servico WHERE {pred}"
        ") f LEFT JOIN analytics.dim_fornecedor d ON d.ni_fornecedor = f.ni_fornecedor "
        "GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 8",
    )
    return tuple(
        LeaderboardRow(str(title), format_brl(float(amount)), index)
        for index, (title, _ni, amount) in enumerate(rows, start=1)
    )


def _cnae_leaders(conn: AnalyticsConnection) -> tuple[LeaderboardRow, ...]:
    rows = fetch_rows(
        conn,
        "SELECT COALESCE(NULLIF(TRIM(nome_cnae), ''), '(sem CNAE)'), COUNT(*) "
        "FROM analytics.dim_fornecedor GROUP BY 1 ORDER BY 2 DESC LIMIT 8",
    )
    return tuple(
        LeaderboardRow(str(title), format_count(int(amount)), index)
        for index, (title, amount) in enumerate(rows, start=1)
    )

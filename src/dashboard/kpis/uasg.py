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

_UF_SQL = (
    "SELECT COALESCE(sigla_uf, '(sem UF)'), COUNT(*) "
    "FROM analytics.dim_uasg GROUP BY 1 ORDER BY 2 DESC LIMIT 8"
)


def load_uasg_kpis(conn: AnalyticsConnection, timeframe: Timeframe) -> ThemeKpis:
    pred = fact_predicate(timeframe)
    uasgs, ativas, sisg, siasg = _catalog_counts(conn)
    orgaos = scalar_int(
        conn, "SELECT COUNT(DISTINCT codigo_orgao) FROM analytics.dim_uasg"
    )
    spend = scalar_float(conn, _spend_sql(pred))
    cards = _uasg_cards(uasgs, ativas, sisg, siasg, orgaos, spend)
    return ThemeKpis(
        cards,
        (_monthly(conn, pred),),
        ranked_with_pct(_label_amounts(conn, _UF_SQL)),
        ranked_with_pct(_sisg_rank_rows(sisg, uasgs)),
        _uasg_leaders(conn, pred),
        _orgao_leaders(conn, pred),
    )


def _catalog_counts(conn: AnalyticsConnection) -> tuple[int, int, int, int]:
    row = fetch_one_row(
        conn,
        "SELECT COUNT(*), "
        "COUNT(*) FILTER (WHERE is_ativo), "
        "COUNT(*) FILTER (WHERE is_uso_sisg), "
        "COUNT(*) FILTER (WHERE is_adesao_siasg) "
        "FROM analytics.dim_uasg",
    )
    return four_ints(row)


def _uasg_cards(
    uasgs: int,
    ativas: int,
    sisg: int,
    siasg: int,
    orgaos: int,
    spend: float,
) -> tuple[KpiCard, ...]:
    return (
        KpiCard("UASGs", format_count(uasgs), "Cadastro"),
        KpiCard("Ativas", format_count(ativas), "Status"),
        KpiCard("Uso SISG", format_count(sisg), "Sistema"),
        KpiCard("Adesão SIASG", format_count(siasg), "Sistema"),
        KpiCard("Órgãos", format_count(orgaos), "codigo_orgao"),
        KpiCard("Valor homologado", format_brl(spend), "Compras"),
    )


def _sisg_rank_rows(sisg: int, uasgs: int) -> list[tuple[str, float]]:
    return [("SISG", float(sisg)), ("Fora do SISG", float(uasgs - sisg))]


def _spend_sql(pred: str) -> str:
    return (
        "SELECT COALESCE(SUM(valor_total_homologado), 0) FROM ("
        f"SELECT valor_total_homologado FROM analytics.fct_preco_material WHERE {pred} "
        "UNION ALL "
        f"SELECT valor_total_homologado FROM analytics.fct_preco_servico WHERE {pred}"
        ") s"
    )


def _monthly(conn: AnalyticsConnection, pred: str) -> NamedSeries:
    rows = fetch_rows(
        conn,
        "SELECT to_char(date_trunc('month', data_compra), 'YYYY-MM'), "
        "COALESCE(SUM(valor_total_homologado), 0) FROM ("
        f"SELECT data_compra, valor_total_homologado FROM analytics.fct_preco_material WHERE {pred} "
        "UNION ALL "
        f"SELECT data_compra, valor_total_homologado FROM analytics.fct_preco_servico WHERE {pred}"
        ") s WHERE data_compra IS NOT NULL GROUP BY 1 ORDER BY 1",
    )
    return NamedSeries(
        "Compras", tuple(SeriesPoint(str(p), float(v)) for p, v in rows)
    )


def _label_amounts(
    conn: AnalyticsConnection, query: str
) -> list[tuple[str, float]]:
    return [(str(label), float(amount)) for label, amount in fetch_rows(conn, query)]


def _uasg_leaders(conn: AnalyticsConnection, pred: str) -> tuple[LeaderboardRow, ...]:
    rows = fetch_rows(
        conn,
        "SELECT COALESCE(u.nome_uasg, f.codigo_uasg), f.codigo_uasg, "
        "SUM(f.valor_total_homologado) FROM ("
        f"SELECT codigo_uasg, valor_total_homologado FROM analytics.fct_preco_material WHERE {pred} "
        "UNION ALL "
        f"SELECT codigo_uasg, valor_total_homologado FROM analytics.fct_preco_servico WHERE {pred}"
        ") f LEFT JOIN analytics.dim_uasg u ON u.codigo_uasg = f.codigo_uasg "
        "GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 8",
    )
    return _leaderboard_from_spend_rows(rows)


def _orgao_leaders(conn: AnalyticsConnection, pred: str) -> tuple[LeaderboardRow, ...]:
    rows = fetch_rows(
        conn,
        "SELECT COALESCE(CAST(u.codigo_orgao AS text), '(sem órgão)'), "
        "CAST(u.codigo_orgao AS text), SUM(f.valor_total_homologado) FROM ("
        f"SELECT codigo_uasg, valor_total_homologado FROM analytics.fct_preco_material WHERE {pred} "
        "UNION ALL "
        f"SELECT codigo_uasg, valor_total_homologado FROM analytics.fct_preco_servico WHERE {pred}"
        ") f JOIN analytics.dim_uasg u ON u.codigo_uasg = f.codigo_uasg "
        "GROUP BY 1, 2 ORDER BY 3 DESC LIMIT 8",
    )
    return _leaderboard_from_spend_rows(rows)


def _leaderboard_from_spend_rows(
    rows: list[tuple[object, ...]],
) -> tuple[LeaderboardRow, ...]:
    return tuple(
        LeaderboardRow(str(title), format_brl(float(amount)), index)
        for index, (title, _code, amount) in enumerate(rows, start=1)
    )

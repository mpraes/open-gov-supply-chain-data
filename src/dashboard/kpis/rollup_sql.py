from etl.ingestion.dest_schema import require_sql_ident

from dashboard.kpis.types import Timeframe

_ORIGENS = frozenset({"material", "servico"})
_TOP_TABELAS = frozenset(
    {"fornecedor", "item_material", "item_servico", "uasg", "orgao"}
)
_JANELAS = frozenset({"all", "12m"})


def require_origem(origem: str) -> str:
    """Accept only the two fact origins used by dashboard rollups.

    Example:
        require_origem("material") == "material"
    """
    if origem not in _ORIGENS:
        raise ValueError(
            f"origem expected one of {set(_ORIGENS)}, got {origem!r}"
        )
    return origem


def sum_origem_sql(origem: str, pred: str) -> str:
    origin = require_origem(origem)
    return (
        "SELECT COALESCE(SUM(valor_total), 0) "
        f"FROM analytics.kpi_mes_origem WHERE origem = '{origin}' AND {pred}"
    )


def sum_both_origens_sql(pred: str) -> str:
    return (
        "SELECT COALESCE(SUM(valor_total), 0) "
        f"FROM analytics.kpi_mes_origem WHERE {pred}"
    )


def monthly_origem_sql(origem: str, pred: str) -> str:
    origin = require_origem(origem)
    return (
        "SELECT to_char(mes, 'YYYY-MM'), COALESCE(SUM(valor_total), 0) "
        f"FROM analytics.kpi_mes_origem WHERE origem = '{origin}' AND {pred} "
        "AND mes IS NOT NULL GROUP BY 1 ORDER BY 1"
    )


def monthly_both_origens_sql(pred: str) -> str:
    return (
        "SELECT to_char(mes, 'YYYY-MM'), COALESCE(SUM(valor_total), 0) "
        f"FROM analytics.kpi_mes_origem WHERE {pred} AND mes IS NOT NULL "
        "GROUP BY 1 ORDER BY 1"
    )


def distinct_key_sql(table: str, key: str, pred: str) -> str:
    ident_table = require_sql_ident(table, "table")
    ident_key = require_sql_ident(key, "column")
    return (
        f"SELECT COUNT(DISTINCT {ident_key}) "
        f"FROM analytics.{ident_table} WHERE {pred}"
    )


def spend_source(timeframe: Timeframe, monthly: str, total: str) -> str:
    """Use pre-summed totals for all-time; monthly grain for the 12m window.

    Example:
        spend_source("all", "kpi_mes_fornecedor", "kpi_fornecedor_total")
    """
    chosen = total if timeframe == "all" else monthly
    return require_sql_ident(chosen, "table")


def distinct_total_sql(
    table: str, key: str, timeframe: Timeframe, *, origem: str | None = None
) -> str:
    ident = require_sql_ident(table, "table")
    ident_key = require_sql_ident(key, "column")
    pred = (
        "TRUE"
        if timeframe == "all"
        else "mes_max >= (CURRENT_DATE - INTERVAL '12 months')"
    )
    extra = ""
    if origem is not None:
        extra = f" AND origem = '{require_origem(origem)}'"
    return (
        f"SELECT COUNT(DISTINCT {ident_key}) "
        f"FROM analytics.{ident} WHERE {pred}{extra}"
    )


def require_qualified_table(value: str) -> str:
    schema, sep, table = value.partition(".")
    if sep != ".":
        raise ValueError(
            f"table expected schema.ident, got {value!r}"
        )
    return f"{require_sql_ident(schema, 'schema')}.{require_sql_ident(table, 'table')}"


def spend_leader_sql(
    table: str,
    key: str,
    label_sql: str,
    dim_table: str,
    pred: str,
    *,
    extra_pred: str = "",
) -> str:
    ident_table = require_sql_ident(table, "table")
    ident_key = require_sql_ident(key, "column")
    dim = require_qualified_table(dim_table)
    extra = f" AND {extra_pred}" if extra_pred else ""
    return (
        f"SELECT COALESCE({label_sql}, CAST(s.{ident_key} AS text)), "
        f"s.{ident_key}, s.valor_total FROM ("
        f"SELECT {ident_key}, SUM(valor_total) AS valor_total "
        f"FROM analytics.{ident_table} WHERE {pred}{extra} "
        "GROUP BY 1 ORDER BY 2 DESC LIMIT 8"
        f") s LEFT JOIN {dim} d ON d.{ident_key} = s.{ident_key}"
    )


def require_janela(timeframe: Timeframe) -> str:
    """Accept only the two dashboard windows stored on snapshot tables.

    Example:
        require_janela("12m") == "12m"
    """
    if timeframe not in _JANELAS:
        raise ValueError(
            f"janela expected one of {set(_JANELAS)}, got {timeframe!r}"
        )
    return timeframe


def require_top_tabela(tabela: str) -> str:
    if tabela not in _TOP_TABELAS:
        raise ValueError(
            f"tabela expected one of {set(_TOP_TABELAS)}, got {tabela!r}"
        )
    return tabela


def priced_count_sql(column: str, timeframe: Timeframe) -> str:
    """Read a precomputed distinct-count column for the selected window.

    Example:
        priced_count_sql("n_fornecedor", "12m")
    """
    ident = require_sql_ident(column, "column")
    janela = require_janela(timeframe)
    return (
        f"SELECT {ident} FROM analytics.kpi_priced_counts "
        f"WHERE janela = '{janela}'"
    )


def top_spend_sql(
    tabela: str, timeframe: Timeframe, *, origem: str = "all"
) -> str:
    """Read precomputed top-8 spend rows; no GROUP BY at request time.

    Example:
        top_spend_sql("item_material", "12m")
    """
    name = require_top_tabela(tabela)
    janela = require_janela(timeframe)
    origin = "all" if origem == "all" else require_origem(origem)
    return (
        "SELECT label, key, valor_total FROM analytics.kpi_top_spend "
        f"WHERE tabela = '{name}' AND janela = '{janela}' "
        f"AND origem = '{origin}' ORDER BY valor_total DESC"
    )

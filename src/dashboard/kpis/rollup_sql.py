"""Monta o SQL dos rollups mensais e snapshots de KPI."""

from etl.ingestion.dest_schema import require_sql_ident

from dashboard.kpis.types import Timeframe

_ORIGENS = frozenset({"material", "servico"})
_TOP_TABELAS = frozenset(
    {"fornecedor", "item_material", "item_servico", "uasg", "orgao"}
)
_JANELAS = frozenset({"all", "12m"})


def require_origem(origem: str) -> str:
    """Aceita só as duas origens de fato usadas nos rollups do dashboard.

    Exemplo:
        require_origem("material") == "material"
    """
    if origem not in _ORIGENS:
        raise ValueError(
            f"origem expected one of {set(_ORIGENS)}, got {origem!r}"
        )
    return origem


def sum_origem_sql(origem: str, pred: str) -> str:
    """Soma valor_total em analytics.kpi_mes_origem para a origem e o predicado pred.

    Exemplo:
        sum_origem_sql("material", "TRUE") == (
            "SELECT COALESCE(SUM(valor_total), 0) "
            "FROM analytics.kpi_mes_origem WHERE origem = 'material' AND TRUE"
        )
    """
    origin = require_origem(origem)
    return (
        "SELECT COALESCE(SUM(valor_total), 0) "
        f"FROM analytics.kpi_mes_origem WHERE origem = '{origin}' AND {pred}"
    )


def sum_both_origens_sql(pred: str) -> str:
    """Soma valor_total em analytics.kpi_mes_origem para material e servico no predicado pred.

    Exemplo:
        sum_both_origens_sql("TRUE") == (
            "SELECT COALESCE(SUM(valor_total), 0) FROM analytics.kpi_mes_origem WHERE TRUE"
        )
    """
    return (
        "SELECT COALESCE(SUM(valor_total), 0) "
        f"FROM analytics.kpi_mes_origem WHERE {pred}"
    )


def monthly_origem_sql(origem: str, pred: str) -> str:
    """Agrupa valor_total de kpi_mes_origem por mês para a origem e o predicado pred.

    Exemplo:
        monthly_origem_sql("material", "TRUE") == (
            "SELECT to_char(mes, 'YYYY-MM'), COALESCE(SUM(valor_total), 0) "
            "FROM analytics.kpi_mes_origem WHERE origem = 'material' AND TRUE "
            "AND mes IS NOT NULL GROUP BY 1 ORDER BY 1"
        )
    """
    origin = require_origem(origem)
    return (
        "SELECT to_char(mes, 'YYYY-MM'), COALESCE(SUM(valor_total), 0) "
        f"FROM analytics.kpi_mes_origem WHERE origem = '{origin}' AND {pred} "
        "AND mes IS NOT NULL GROUP BY 1 ORDER BY 1"
    )


def monthly_both_origens_sql(pred: str) -> str:
    """Agrupa valor_total de kpi_mes_origem por mês para material e servico no predicado pred.

    Exemplo:
        monthly_both_origens_sql("TRUE") == (
            "SELECT to_char(mes, 'YYYY-MM'), COALESCE(SUM(valor_total), 0) "
            "FROM analytics.kpi_mes_origem WHERE TRUE AND mes IS NOT NULL "
            "GROUP BY 1 ORDER BY 1"
        )
    """
    return (
        "SELECT to_char(mes, 'YYYY-MM'), COALESCE(SUM(valor_total), 0) "
        f"FROM analytics.kpi_mes_origem WHERE {pred} AND mes IS NOT NULL "
        "GROUP BY 1 ORDER BY 1"
    )


def distinct_key_sql(table: str, key: str, pred: str) -> str:
    """Conta chaves distintas de uma tabela de analytics filtrada por pred.

    Exemplo:
        distinct_key_sql("kpi_mes_origem", "origem", "TRUE") == (
            "SELECT COUNT(DISTINCT origem) FROM analytics.kpi_mes_origem WHERE TRUE"
        )
    """
    ident_table = require_sql_ident(table, "table")
    ident_key = require_sql_ident(key, "column")
    return (
        f"SELECT COUNT(DISTINCT {ident_key}) "
        f"FROM analytics.{ident_table} WHERE {pred}"
    )


def spend_source(timeframe: Timeframe, monthly: str, total: str) -> str:
    """Usa totais pré-somados no período completo; granularidade mensal na janela de 12 meses.

    Exemplo:
        spend_source("all", "kpi_mes_fornecedor", "kpi_fornecedor_total")
    """
    chosen = total if timeframe == "all" else monthly
    return require_sql_ident(chosen, "table")


def distinct_total_sql(
    table: str, key: str, timeframe: Timeframe,     *, origem: str | None = None
) -> str:
    """Conta chaves distintas na janela, filtrando origem quando ela é informada.

    Exemplo:
        distinct_total_sql("kpi_fornecedor_janela", "n_fornecedor", "all") == (
            "SELECT COUNT(DISTINCT n_fornecedor) "
            "FROM analytics.kpi_fornecedor_janela WHERE TRUE"
        )
    """
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
    """Exige schema.ident e devolve os dois identificadores validados.

    Exemplo:
        require_qualified_table("analytics.dim_fornecedor") == "analytics.dim_fornecedor"
    """
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
    """Monta o top 8 de gasto com rótulo vindo do LEFT JOIN na dimensão.

    Exemplo:
        spend_leader_sql(
            "kpi_mes_fornecedor", "codigo", "d.nome", "analytics.dim_fornecedor", "TRUE"
        ) == (
            "SELECT COALESCE(d.nome, CAST(s.codigo AS text)), s.codigo, s.valor_total "
            "FROM (SELECT codigo, SUM(valor_total) AS valor_total "
            "FROM analytics.kpi_mes_fornecedor WHERE TRUE "
            "GROUP BY 1 ORDER BY 2 DESC LIMIT 8) s "
            "LEFT JOIN analytics.dim_fornecedor d ON d.codigo = s.codigo"
        )
    """
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
    """Aceita só as duas janelas do dashboard gravadas nas tabelas de snapshot.

    Exemplo:
        require_janela("12m") == "12m"
    """
    if timeframe not in _JANELAS:
        raise ValueError(
            f"janela expected one of {set(_JANELAS)}, got {timeframe!r}"
        )
    return timeframe


def require_top_tabela(tabela: str) -> str:
    """Aceita só as tabelas de snapshot do ranking de gasto.

    Exemplo:
        require_top_tabela("fornecedor") == "fornecedor"
    """
    if tabela not in _TOP_TABELAS:
        raise ValueError(
            f"tabela expected one of {set(_TOP_TABELAS)}, got {tabela!r}"
        )
    return tabela


def priced_count_sql(column: str, timeframe: Timeframe) -> str:
    """Lê a coluna de contagem distinta pré-calculada da janela selecionada.

    Exemplo:
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
    """Lê as 8 linhas de gasto pré-calculadas; sem GROUP BY na hora da requisição.

    Exemplo:
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

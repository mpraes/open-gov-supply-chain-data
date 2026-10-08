from dashboard.kpis.rollup_sql import (
    distinct_key_sql,
    distinct_total_sql,
    monthly_both_origens_sql,
    monthly_origem_sql,
    priced_count_sql,
    require_origem,
    require_qualified_table,
    spend_leader_sql,
    spend_source,
    sum_both_origens_sql,
    sum_origem_sql,
    top_spend_sql,
)
import pytest


def test_require_origem_rejects_unknown_value() -> None:
    with pytest.raises(ValueError, match=r"got 'staging'"):
        require_origem("staging")


def test_sum_origem_sql_reads_kpi_mes_origem() -> None:
    sql = sum_origem_sql("material", "TRUE")
    assert "analytics.kpi_mes_origem" in sql
    assert "fct_preco_" not in sql
    assert "origem = 'material'" in sql


def test_sum_both_and_monthly_sql_stay_on_rollup() -> None:
    assert "kpi_mes_origem" in sum_both_origens_sql("TRUE")
    assert "kpi_mes_origem" in monthly_both_origens_sql("TRUE")
    monthly = monthly_origem_sql("servico", "mes >= CURRENT_DATE")
    assert "kpi_mes_origem" in monthly
    assert "origem = 'servico'" in monthly


def test_distinct_key_sql_uses_named_rollup() -> None:
    sql = distinct_key_sql("kpi_mes_fornecedor", "ni_fornecedor", "TRUE")
    assert "COUNT(DISTINCT ni_fornecedor)" in sql
    assert "analytics.kpi_mes_fornecedor" in sql
    assert "fct_preco_" not in sql


def test_distinct_total_sql_all_counts_distinct_key() -> None:
    sql = distinct_total_sql("kpi_fornecedor_total", "ni_fornecedor", "all")
    assert "COUNT(DISTINCT ni_fornecedor)" in sql
    assert "kpi_fornecedor_total" in sql
    assert "mes_max" not in sql


def test_distinct_total_sql_12m_uses_mes_max() -> None:
    sql = distinct_total_sql("kpi_item_material_total", "cod_item", "12m")
    assert "mes_max" in sql
    assert "12 months" in sql
    assert "COUNT(DISTINCT cod_item)" in sql


def test_spend_source_picks_total_for_all() -> None:
    assert spend_source("all", "kpi_mes_fornecedor", "kpi_fornecedor_total") == (
        "kpi_fornecedor_total"
    )
    assert spend_source("12m", "kpi_mes_fornecedor", "kpi_fornecedor_total") == (
        "kpi_mes_fornecedor"
    )


def test_require_qualified_table_rejects_bare_name() -> None:
    with pytest.raises(ValueError, match=r"got 'dim_fornecedor'"):
        require_qualified_table("dim_fornecedor")


def test_spend_leader_sql_aggregates_before_dim_join() -> None:
    sql = spend_leader_sql(
        "kpi_fornecedor_total",
        "ni_fornecedor",
        "d.nome_razao_social",
        "analytics.dim_fornecedor",
        "TRUE",
    )
    assert "GROUP BY 1" in sql
    assert sql.index("GROUP BY 1") < sql.index("dim_fornecedor")
    assert "LIMIT 8" in sql


def test_priced_count_sql_reads_snapshot_by_janela() -> None:
    sql = priced_count_sql("n_fornecedor", "12m")
    assert "analytics.kpi_priced_counts" in sql
    assert "n_fornecedor" in sql
    assert "janela = '12m'" in sql
    assert "COUNT(" not in sql


def test_top_spend_sql_filters_precomputed_leaders() -> None:
    sql = top_spend_sql("item_material", "12m")
    assert "analytics.kpi_top_spend" in sql
    assert "tabela = 'item_material'" in sql
    assert "janela = '12m'" in sql
    assert "origem = 'all'" in sql
    assert "GROUP BY" not in sql


def test_top_spend_sql_rejects_unknown_tabela() -> None:
    with pytest.raises(ValueError, match=r"got 'fact'"):
        top_spend_sql("fact", "all")

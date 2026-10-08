from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ROLLUPS = ROOT / "src/sql/refresh_dashboard_kpi_rollups.sql"
INDEXES = ROOT / "src/sql/create_dashboard_fact_indexes.sql"


def test_refresh_script_builds_slim_then_named_rollups() -> None:
    text = ROLLUPS.read_text(encoding="utf-8")
    for needle in (
        "analytics._kpi_mat_slim",
        "analytics._kpi_srv_slim",
        "analytics.kpi_mes_origem",
        "analytics.kpi_mes_fornecedor",
        "analytics.kpi_mes_uasg",
        "analytics.kpi_mes_item_material",
        "analytics.kpi_mes_item_servico",
        "analytics.kpi_mes_grupo_material",
        "analytics.kpi_mes_grupo_servico",
        "analytics.kpi_fornecedor_total",
        "analytics.kpi_catalog_fornecedor",
        "analytics.kpi_catalog_overview",
        "analytics.kpi_catalog_servico",
        "analytics.kpi_catalog_uasg",
        "analytics.kpi_priced_counts",
        "analytics.kpi_top_spend",
    ):
        assert needle in text
    assert "fct_preco_material" in text
    assert "DROP TABLE IF EXISTS analytics._kpi_mat_slim" in text


def test_index_script_covers_fact_filter_and_join_keys() -> None:
    text = INDEXES.read_text(encoding="utf-8")
    assert "CREATE INDEX CONCURRENTLY" in text
    assert "fct_preco_material" in text
    assert "fct_preco_servico" in text
    assert "data_compra" in text
    assert "valor_total_homologado" in text
    assert "ni_fornecedor" in text
    assert "codigo_uasg" in text

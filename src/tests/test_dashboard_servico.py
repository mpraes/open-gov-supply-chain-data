from fakes.analytics_db import FakeAnalyticsConnection

from dashboard.kpis.servico import load_servico_kpis


def test_load_servico_kpis_uses_stg_for_ranked_section() -> None:
    conn = FakeAnalyticsConnection(
        result_sets=[
            [(3102, 3019, 3, 0.0361)],
            [(80.0,)],
            [(4,)],
            [("2026-01", 1.0)],
            [("Construção", 6)],
            [("Grupo A", 10.0)],
            [("Limpeza", "2", 9.0)],
            [("Fornecedor B", "9", 3.0)],
        ]
    )
    payload = load_servico_kpis(conn, "all")
    assert payload.cards[0].label == "Serviços"
    assert payload.cards[2].label == "Cobertura hierarquia"
    assert "3,6%" in payload.cards[2].value or payload.cards[2].value == "3,6%"
    assert payload.ranked_left[0].label == "Construção"
    assert payload.ranked_right[0].value.startswith("R$")
    assert payload.leaderboard_left[0].subtitle.startswith("R$")
    assert payload.leaderboard_right[0].subtitle.startswith("R$")
    assert "kpi_catalog_servico" in conn.cursor_obj.queries[0]
    ranked_sql = conn.cursor_obj.queries[4]
    assert "kpi_servico_secao" in ranked_sql
    assert "stg_servico_item" not in ranked_sql
    fact_sql = " ".join(conn.cursor_obj.queries[1:])
    assert "kpi_mes_" in fact_sql
    assert "kpi_top_spend" in fact_sql
    assert "fct_preco_" not in fact_sql

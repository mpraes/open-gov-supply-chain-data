from fakes.analytics_db import FakeAnalyticsConnection

from dashboard.kpis.material import load_material_kpis


def test_load_material_kpis_maps_catalog_and_spend() -> None:
    conn = FakeAnalyticsConnection(
        result_sets=[
            [(345001, 249470, 584, 51587)],
            [(99.0,)],
            [(12,)],
            [("2026-01", 9.0)],
            [("Médico", 100)],
            [("Médico", 50.0)],
            [("Gaze", 1, 10.0)],
            [("Fornecedor A", "1", 8.0)],
        ]
    )
    payload = load_material_kpis(conn, "all")
    assert payload.cards[0].label == "Itens"
    assert payload.cards[2].label == "Sustentáveis"
    assert payload.series[0].name == "Material"
    assert payload.ranked_left[0].label == "Médico"
    assert payload.ranked_right[0].value.startswith("R$")
    assert payload.leaderboard_left[0].title == "Gaze"
    assert payload.leaderboard_left[0].subtitle.startswith("R$")
    assert payload.leaderboard_right[0].title == "Fornecedor A"
    assert payload.leaderboard_right[0].subtitle.startswith("R$")
    fact_sql = " ".join(conn.cursor_obj.queries[1:])
    assert "kpi_mes_" in fact_sql
    assert "fct_preco_" not in fact_sql
    assert "kpi_priced_counts" in conn.cursor_obj.queries[2]
    assert "kpi_top_spend" in conn.cursor_obj.queries[6]
    assert "kpi_top_spend" in conn.cursor_obj.queries[7]

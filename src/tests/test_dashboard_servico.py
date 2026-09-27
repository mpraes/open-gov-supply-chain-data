from fakes.analytics_db import FakeAnalyticsConnection

from dashboard.kpis.servico import load_servico_kpis


def test_load_servico_kpis_uses_stg_for_ranked_section() -> None:
    conn = FakeAnalyticsConnection(
        result_sets=[
            [(3102, 3019, 3)],
            [(3102, 112)],
            [(80.0,)],
            [(4,)],
            [("2026-01", 1.0)],
            [("Construção", 6)],
            [("Grupo A", 10.0)],
            [("Limpeza", 9.0)],
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
    ranked_sql = conn.cursor_obj.queries[5]
    assert "stg_servico_item" in ranked_sql

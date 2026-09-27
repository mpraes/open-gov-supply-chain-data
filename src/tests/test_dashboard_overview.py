from fakes.analytics_db import FakeAnalyticsConnection

from dashboard.kpis.overview import load_overview_kpis


def test_load_overview_kpis_maps_cards_and_two_series() -> None:
    conn = FakeAnalyticsConnection(
        result_sets=[
            [(10,)],
            [(20,)],
            [(30,)],
            [(40,)],
            [(100.0,)],
            [(50.0,)],
            [("2026-01", 10.0), ("2026-02", 20.0)],
            [("2026-01", 5.0)],
        ]
    )
    payload = load_overview_kpis(conn, "all")
    assert [card.label for card in payload.cards] == [
        "Fornecedores",
        "Materiais",
        "Serviços",
        "UASGs",
        "Valor material",
        "Valor serviço",
    ]
    assert payload.cards[0].value == "10"
    assert len(payload.series) == 2
    assert payload.series[0].name == "Material"
    assert payload.ranked_left == ()
    assert payload.leaderboard_right == ()


def test_load_overview_kpis_12m_adds_data_compra_predicate() -> None:
    conn = FakeAnalyticsConnection(
        result_sets=[
            [(0,)],
            [(0,)],
            [(0,)],
            [(0,)],
            [(0,)],
            [(0,)],
            [],
            [],
        ]
    )
    load_overview_kpis(conn, "12m")
    fact_sql = " ".join(conn.cursor_obj.queries[4:])
    assert "12 months" in fact_sql

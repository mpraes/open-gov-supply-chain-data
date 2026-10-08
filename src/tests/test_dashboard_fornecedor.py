from fakes.analytics_db import FakeAnalyticsConnection

from dashboard.kpis.fornecedor import load_fornecedor_kpis


def test_load_fornecedor_kpis_fills_six_cards_and_lists() -> None:
    conn = FakeAnalyticsConnection(
        result_sets=[
            [(100, 80, 70, 5)],
            [(1000.0,)],
            [(12,)],
            [("2026-01", 1.0)],
            [("2026-01", 2.0)],
            [("SP", 60), ("RJ", 40)],
            [("MICROEMPRESA", 70), ("DEMAIS", 30)],
            [("ACME", "123", 500.0)],
            [("Construção", 20)],
        ]
    )
    payload = load_fornecedor_kpis(conn, "all")
    assert payload.cards[0].label == "Fornecedores"
    assert payload.cards[2].label == "Habilitados"
    assert payload.ranked_left[0].label == "SP"
    assert payload.leaderboard_left[0].title == "ACME"
    assert payload.leaderboard_left[0].subtitle.startswith("R$")
    assert payload.leaderboard_right[0].title == "Construção"
    assert payload.leaderboard_right[0].subtitle == "20"
    priced_sql = conn.cursor_obj.queries[2]
    assert "kpi_priced_counts" in priced_sql
    assert "COUNT(" not in priced_sql
    assert "kpi_top_spend" in conn.cursor_obj.queries[7]


def test_load_fornecedor_kpis_12m_predicate_on_fact_queries() -> None:
    conn = FakeAnalyticsConnection(
        result_sets=[
            [(0, 0, 0, 0)],
            [(0,)],
            [(0,)],
            [],
            [],
            [],
            [],
            [],
            [],
        ]
    )
    load_fornecedor_kpis(conn, "12m")
    fact_sql = " ".join(conn.cursor_obj.queries[1:])
    assert "janela = '12m'" in fact_sql
    assert "kpi_mes_" in fact_sql
    assert "fct_preco_" not in fact_sql

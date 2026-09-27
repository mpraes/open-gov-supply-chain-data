from fakes.analytics_db import FakeAnalyticsConnection

from dashboard.kpis.uasg import load_uasg_kpis


def test_load_uasg_kpis_maps_buyer_cards() -> None:
    conn = FakeAnalyticsConnection(
        result_sets=[
            [(45592, 22092, 22289, 41052)],
            [(12000,)],
            [(200.0,)],
            [("2026-01", 20.0)],
            [("SP", 5440)],
            [("UASG 1", "100", 9.0)],
            [("Órgão 1", "50", 8.0)],
        ]
    )
    payload = load_uasg_kpis(conn, "all")
    assert payload.cards[0].label == "UASGs"
    assert payload.cards[2].label == "Uso SISG"
    assert payload.ranked_left[0].label == "SP"
    assert payload.ranked_right[0].label == "SISG"
    assert payload.leaderboard_left[0].title == "UASG 1"
    assert payload.leaderboard_right[0].title == "Órgão 1"

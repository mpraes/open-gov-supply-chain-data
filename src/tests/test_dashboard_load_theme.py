import pytest
from fakes.analytics_db import FakeAnalyticsConnection

from dashboard.kpis.load_theme import THEMES, _LOADERS, load_theme_kpis, theme_kpis_json
from dashboard.kpis.types import KpiCard, ThemeKpis


def test_themes_are_the_five_routes() -> None:
    assert THEMES == ("overview", "fornecedor", "material", "servico", "uasg")
    assert set(_LOADERS) == set(THEMES)


def test_load_theme_kpis_overview_returns_six_cards() -> None:
    conn = FakeAnalyticsConnection(
        result_sets=[
            [(10, 20, 30, 40)],
            [(100.0,)],
            [(50.0,)],
            [("2026-01", 10.0)],
            [("2026-01", 5.0)],
        ]
    )
    payload = load_theme_kpis("overview", conn, "all")
    assert len(payload.cards) == 6


def test_load_theme_kpis_rejects_unknown_theme() -> None:
    conn = FakeAnalyticsConnection(result_sets=[])
    with pytest.raises(ValueError, match=r"got 'contratos'"):
        load_theme_kpis("contratos", conn, "all")


def test_theme_kpis_json_serializes_cards() -> None:
    payload = ThemeKpis(
        cards=(KpiCard("A", "1", "h"),),
        series=(),
        ranked_left=(),
        ranked_right=(),
        leaderboard_left=(),
        leaderboard_right=(),
    )
    body = theme_kpis_json(payload)
    assert body["cards"] == [{"label": "A", "value": "1", "hint": "h"}]

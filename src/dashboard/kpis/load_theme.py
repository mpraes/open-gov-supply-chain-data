from collections.abc import Callable
from dataclasses import asdict

from dashboard.db import AnalyticsConnection
from dashboard.kpis.fornecedor import load_fornecedor_kpis
from dashboard.kpis.material import load_material_kpis
from dashboard.kpis.overview import load_overview_kpis
from dashboard.kpis.servico import load_servico_kpis
from dashboard.kpis.types import ThemeKpis, Timeframe
from dashboard.kpis.uasg import load_uasg_kpis

THEMES = ("overview", "fornecedor", "material", "servico", "uasg")

_LOADERS: dict[str, Callable[[AnalyticsConnection, Timeframe], ThemeKpis]] = {
    "overview": load_overview_kpis,
    "fornecedor": load_fornecedor_kpis,
    "material": load_material_kpis,
    "servico": load_servico_kpis,
    "uasg": load_uasg_kpis,
}


def load_theme_kpis(
    theme: str, conn: AnalyticsConnection, timeframe: Timeframe
) -> ThemeKpis:
    loader = _LOADERS.get(theme)
    if loader is None:
        raise ValueError(f"theme expected one of {set(THEMES)}, got {theme!r}")
    return loader(conn, timeframe)


def theme_kpis_json(payload: ThemeKpis) -> dict[str, object]:
    return {
        "cards": [asdict(card) for card in payload.cards],
        "series": [asdict(series) for series in payload.series],
        "ranked_left": [asdict(row) for row in payload.ranked_left],
        "ranked_right": [asdict(row) for row in payload.ranked_right],
        "leaderboard_left": [asdict(row) for row in payload.leaderboard_left],
        "leaderboard_right": [asdict(row) for row in payload.leaderboard_right],
    }

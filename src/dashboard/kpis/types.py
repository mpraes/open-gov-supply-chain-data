from dataclasses import dataclass
from typing import Literal

Timeframe = Literal["all", "12m"]


@dataclass(frozen=True)
class KpiCard:
    label: str
    value: str
    hint: str


@dataclass(frozen=True)
class SeriesPoint:
    period: str
    value: float


@dataclass(frozen=True)
class NamedSeries:
    name: str
    points: tuple[SeriesPoint, ...]


@dataclass(frozen=True)
class RankedRow:
    label: str
    value: str
    pct: float


@dataclass(frozen=True)
class LeaderboardRow:
    title: str
    subtitle: str
    rank: int


@dataclass(frozen=True)
class ThemeKpis:
    cards: tuple[KpiCard, ...]
    series: tuple[NamedSeries, ...]
    ranked_left: tuple[RankedRow, ...]
    ranked_right: tuple[RankedRow, ...]
    leaderboard_left: tuple[LeaderboardRow, ...]
    leaderboard_right: tuple[LeaderboardRow, ...]

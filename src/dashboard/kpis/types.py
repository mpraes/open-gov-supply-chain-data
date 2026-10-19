"""Tipos imutáveis do payload de KPIs do dashboard."""

from dataclasses import dataclass
from typing import Literal

Timeframe = Literal["all", "12m"]


@dataclass(frozen=True)
class KpiCard:
    """Cartão de KPI com rótulo, valor formatado e dica."""

    label: str
    value: str
    hint: str


@dataclass(frozen=True)
class SeriesPoint:
    """Ponto de uma série temporal com período e valor numérico."""

    period: str
    value: float


@dataclass(frozen=True)
class NamedSeries:
    """Série nomeada de pontos para o gráfico do tema."""

    name: str
    points: tuple[SeriesPoint, ...]


@dataclass(frozen=True)
class RankedRow:
    """Barra de ranking com rótulo, valor formatado e percentual do pico."""

    label: str
    value: str
    pct: float


@dataclass(frozen=True)
class LeaderboardRow:
    """Linha de ranking com título, subtítulo e posição."""

    title: str
    subtitle: str
    rank: int


@dataclass(frozen=True)
class ThemeKpis:
    """Payload de um tema: cards, séries, dois rankings e dois leaderboards."""

    cards: tuple[KpiCard, ...]
    series: tuple[NamedSeries, ...]
    ranked_left: tuple[RankedRow, ...]
    ranked_right: tuple[RankedRow, ...]
    leaderboard_left: tuple[LeaderboardRow, ...]
    leaderboard_right: tuple[LeaderboardRow, ...]

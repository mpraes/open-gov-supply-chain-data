"""Monta cron e data inicial para ingestões a cada dois dias em São Paulo."""

from datetime import datetime
from zoneinfo import ZoneInfo

_SAO_PAULO = ZoneInfo("America/Sao_Paulo")
_START_DAY = datetime(2026, 9, 27, tzinfo=_SAO_PAULO)


def every_two_days_at(
    hour: int, minute: int, *, days: str = "odd"
) -> tuple[str, datetime]:
    """Cron e data inicial para horários no estilo 08:00, a cada dois dias corridos, em São Paulo.

    Exemplo:
        every_two_days_at(8, 15)[0] == "15 8 */2 * *"
    """
    if hour not in range(24) or minute not in range(60):
        raise ValueError(
            f"hour/minute expected 0-23 and 0-59, got hour={hour!r} minute={minute!r}"
        )
    if days not in {"odd", "even"}:
        raise ValueError(f"days expected 'odd' or 'even', got {days!r}")
    day_cron = "*/2" if days == "odd" else "2-30/2"
    cron = f"{minute} {hour} {day_cron} * *"
    return cron, _START_DAY.replace(hour=hour, minute=minute)

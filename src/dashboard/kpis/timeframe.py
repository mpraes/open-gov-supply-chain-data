from etl.ingestion.dest_schema import require_sql_ident

from dashboard.kpis.types import Timeframe

_ALLOWED = ("all", "12m")


def parse_timeframe(value: str) -> Timeframe:
    if value not in _ALLOWED:
        raise ValueError(
            f"timeframe expected one of {set(_ALLOWED)}, got {value!r}"
        )
    return value


def fact_predicate(timeframe: Timeframe, column: str = "data_compra") -> str:
    ident = require_sql_ident(column, "column")
    if timeframe == "all":
        return "TRUE"
    return f"{ident} >= (CURRENT_DATE - INTERVAL '12 months')"


def mes_predicate(timeframe: Timeframe) -> str:
    """Filter monthly KPI rollups; 12m uses month start, not purchase date.

    Example:
        mes_predicate("all") == "TRUE"
    """
    return fact_predicate(timeframe, "mes")

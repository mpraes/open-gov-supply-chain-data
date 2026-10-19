"""Janelas de tempo e predicados SQL dos KPIs do dashboard."""

from etl.ingestion.dest_schema import require_sql_ident

from dashboard.kpis.types import Timeframe

_ALLOWED = ("all", "12m")


def parse_timeframe(value: str) -> Timeframe:
    """Aceita só as janelas all e 12m.

    Exemplo:
        parse_timeframe("12m") == "12m"
    """
    if value not in _ALLOWED:
        raise ValueError(
            f"timeframe expected one of {set(_ALLOWED)}, got {value!r}"
        )
    return value


def fact_predicate(timeframe: Timeframe, column: str = "data_compra") -> str:
    """Devolve TRUE no período completo e, em 12m, um filtro de 12 meses na coluna.

    Exemplo:
        fact_predicate("12m") == "data_compra >= (CURRENT_DATE - INTERVAL '12 months')"
    """
    ident = require_sql_ident(column, "column")
    if timeframe == "all":
        return "TRUE"
    return f"{ident} >= (CURRENT_DATE - INTERVAL '12 months')"


def mes_predicate(timeframe: Timeframe) -> str:
    """Filtra os rollups mensais de KPI; a janela de 12 meses usa o início do mês, não a data da compra.

    Exemplo:
        mes_predicate("all") == "TRUE"
    """
    return fact_predicate(timeframe, "mes")

"""Formata contagens, valores em reais e rankings dos KPIs do dashboard."""

from collections.abc import Callable

from dashboard.kpis.types import LeaderboardRow, RankedRow


def format_count(value: int | float) -> str:
    """Formata um inteiro com separador de milhar por ponto.

    Exemplo:
        format_count(1234) == "1.234"
    """
    return f"{int(value):,}".replace(",", ".")


def format_brl(value: float) -> str:
    """Formata um valor em reais, abreviando milhão, bilhão e trilhão.

    Exemplo:
        format_brl(10) == "R$ 10,00"
    """
    abs_value = abs(value)
    if abs_value >= 1_000_000_000_000:
        return f"R$ {value / 1_000_000_000_000:.2f} tri".replace(".", ",")
    if abs_value >= 1_000_000_000:
        return f"R$ {value / 1_000_000_000:.2f} bi".replace(".", ",")
    if abs_value >= 1_000_000:
        return f"R$ {value / 1_000_000:.2f} mi".replace(".", ",")
    formatted = f"{value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatted}"


def format_pct(ratio: float) -> str:
    """Formata uma razão como percentual com uma casa e vírgula decimal.

    Exemplo:
        format_pct(0.5) == "50,0%"
    """
    return f"{ratio * 100:.1f}%".replace(".", ",")


def ranked_with_pct(
    rows: list[tuple[str, float]],
    formatter: Callable[[float], str] = format_count,
) -> tuple[RankedRow, ...]:
    """Monta RankedRow com o valor formatado e o percentual em relação ao maior valor.

    Exemplo:
        ranked_with_pct([("A", 10.0), ("B", 5.0)])[1].pct == 50.0
    """
    peak = max((amount for _label, amount in rows), default=0.0)
    return tuple(
        RankedRow(
            label=label,
            value=formatter(amount),
            pct=(amount / peak * 100.0) if peak else 0.0,
        )
        for label, amount in rows
    )


def brl_leaderboard(rows: list[tuple[object, ...]]) -> tuple[LeaderboardRow, ...]:
    """Mapeia linhas de snapshot (rótulo, chave, valor) para cartões de BRL ordenados.

    Exemplo:
        brl_leaderboard([("ACME", "1", 500.0)])[0].rank == 1
    """
    return tuple(
        LeaderboardRow(str(title), format_brl(float(amount)), index)
        for index, (title, _key, amount) in enumerate(rows, start=1)
    )

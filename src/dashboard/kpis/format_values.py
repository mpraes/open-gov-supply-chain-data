from dashboard.kpis.types import RankedRow


def format_count(value: int) -> str:
    return f"{value:,}".replace(",", ".")


def format_brl(value: float) -> str:
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
    return f"{ratio * 100:.1f}%".replace(".", ",")


def ranked_with_pct(rows: list[tuple[str, float]]) -> tuple[RankedRow, ...]:
    peak = max((amount for _label, amount in rows), default=0.0)
    return tuple(
        RankedRow(
            label=label,
            value=format_count(int(amount)),
            pct=(amount / peak * 100.0) if peak else 0.0,
        )
        for label, amount in rows
    )

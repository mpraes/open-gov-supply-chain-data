from dashboard.kpis.format_values import format_brl, format_count, format_pct, ranked_with_pct


def test_format_count_uses_dot_thousands() -> None:
    assert format_count(1016975) == "1.016.975"


def test_format_brl_compact_billions() -> None:
    assert format_brl(666165268174.13).startswith("R$")


def test_format_pct_one_decimal() -> None:
    assert format_pct(0.723) == "72,3%"


def test_ranked_with_pct_scales_to_peak() -> None:
    rows = ranked_with_pct([("SP", 100.0), ("RJ", 50.0)])
    assert rows[0].label == "SP"
    assert rows[0].pct == 100.0
    assert rows[1].pct == 50.0

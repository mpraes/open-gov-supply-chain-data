from dashboard.kpis.format_values import (
    brl_leaderboard,
    format_brl,
    format_count,
    format_pct,
    ranked_with_pct,
)


def test_format_count_uses_dot_thousands() -> None:
    assert format_count(1016975) == "1.016.975"


def test_format_brl_compact_trillions() -> None:
    assert format_brl(1_500_000_000_000) == "R$ 1,50 tri"


def test_format_brl_compact_billions() -> None:
    assert format_brl(666165268174.13) == "R$ 666,17 bi"


def test_format_brl_compact_millions() -> None:
    assert format_brl(2_500_000) == "R$ 2,50 mi"


def test_format_pct_one_decimal() -> None:
    assert format_pct(0.723) == "72,3%"


def test_ranked_with_pct_scales_to_peak() -> None:
    rows = ranked_with_pct([("SP", 100.0), ("RJ", 50.0)])
    assert rows[0].label == "SP"
    assert rows[0].pct == 100.0
    assert rows[1].pct == 50.0
    assert rows[0].value == "100"


def test_ranked_with_pct_spend_uses_brl() -> None:
    rows = ranked_with_pct([("Grupo", 2_500_000.0)], formatter=format_brl)
    assert rows[0].value.startswith("R$")
    assert rows[0].value == "R$ 2,50 mi"


def test_brl_leaderboard_ranks_snapshot_rows() -> None:
    rows = brl_leaderboard([("ACME", "1", 500.0), ("Beta", "2", 50.0)])
    assert rows[0].title == "ACME"
    assert rows[0].rank == 1
    assert rows[0].subtitle.startswith("R$")
    assert rows[1].rank == 2

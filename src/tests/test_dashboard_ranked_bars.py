from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DASHBOARD_JS = ROOT / "src/dashboard/static/dashboard.js"
DASHBOARD_CSS = ROOT / "src/dashboard/static/dashboard.css"


def test_ranked_value_goes_to_rank_value_not_bar_fill() -> None:
    text = DASHBOARD_JS.read_text(encoding="utf-8")
    assert 'class="rank-value"' in text
    assert 'querySelector(".rank-value")' in text


def test_ranked_bar_is_tall_enough_for_label() -> None:
    text = DASHBOARD_CSS.read_text(encoding="utf-8")
    assert ".bar {\n  height: 22px;" in text

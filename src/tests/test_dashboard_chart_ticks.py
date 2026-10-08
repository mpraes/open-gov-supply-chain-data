import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TICKS = ROOT / "src/dashboard/static/chart_ticks.js"
DASHBOARD_JS = ROOT / "src/dashboard/static/dashboard.js"
PAGE = ROOT / "src/dashboard/templates/page.html"


def _eval_ticks(expr: str) -> object:
    script = f"{TICKS.read_text(encoding='utf-8')}\nprocess.stdout.write(JSON.stringify({expr}))"
    raw = subprocess.check_output(["node", "-e", script], text=True)
    return json.loads(raw)


def test_period_to_unix_is_utc_month_start() -> None:
    unix = _eval_ticks('periodToUnix("2026-01")')
    assert unix == 1767225600


def test_period_to_unix_rejects_bad_shape() -> None:
    script = (
        f"{TICKS.read_text(encoding='utf-8')}\n"
        "try { periodToUnix('2026/01'); process.exit(2); }"
        "catch (err) { process.stdout.write(err.message); }"
    )
    message = subprocess.check_output(["node", "-e", script], text=True)
    assert "2026/01" in message
    assert "YYYY-MM" in message


def test_format_month_tick_roundtrips_period() -> None:
    assert _eval_ticks('formatMonthTick(periodToUnix("2024-12"))') == "2024-12"


def test_format_brl_tick_matches_card_compact_units() -> None:
    assert _eval_ticks("formatBrlTick(1500000000000)") == "R$ 1,50 tri"
    assert _eval_ticks("formatBrlTick(666165268174.13)") == "R$ 666,17 bi"
    assert _eval_ticks("formatBrlTick(2500000)") == "R$ 2,50 mi"
    assert _eval_ticks("formatBrlTick(1234.5)") == "R$ 1.234,50"


def test_dashboard_js_maps_periods_to_unix_and_formats_axes() -> None:
    text = DASHBOARD_JS.read_text(encoding="utf-8")
    assert "periodToUnix" in text
    assert "formatMonthTick" in text
    assert "formatBrlTick" in text
    assert "axes:" in text


def test_page_loads_chart_ticks_before_dashboard_js() -> None:
    html = PAGE.read_text(encoding="utf-8")
    ticks_at = html.index("chart_ticks.js")
    dash_at = html.index("dashboard.js")
    assert ticks_at < dash_at

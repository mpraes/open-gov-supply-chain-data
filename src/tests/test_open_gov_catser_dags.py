from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import sys

import pytest

DAGS_DIR = Path(__file__).resolve().parents[2] / "dags"
sys.path.insert(0, str(DAGS_DIR))

from open_gov_schedule import every_two_days_at

CATSER_SCRIPTS = (
    "servico_secao",
    "servico_divisao",
    "servico_grupo",
    "servico_classe",
    "servico_subclasse",
    "servico_item",
    "servico_unidade_medida",
    "servico_natureza_despesa",
)


@pytest.mark.parametrize("script", CATSER_SCRIPTS)
def test_catser_dag_is_manual_airflow3_task(script: str) -> None:
    src = (DAGS_DIR / f"open_gov_{script}.py").read_text(encoding="utf-8")
    assert f'dag_id="open_gov_{script}"' in src
    assert "register_ingest_dag" in src
    assert f"etl.ingestion.servico.{script}" in src
    assert 'tags=["open-gov", "catser"]' in src
    # Airflow dag_discovery_safe_mode only parses files containing "airflow".
    assert "airflow" in src.lower()
    # Airflow loads the file without adding its directory to sys.path.
    assert "sys.path.insert(0, str(Path(__file__).resolve().parent))" in src


def test_every_two_days_at_builds_sao_paulo_cron() -> None:
    cron, start = every_two_days_at(8, 15)
    assert cron == "15 8 */2 * *"
    assert start == datetime(2026, 9, 27, 8, 15, tzinfo=ZoneInfo("America/Sao_Paulo"))


def test_every_two_days_at_rejects_invalid_clock() -> None:
    with pytest.raises(ValueError, match=r"got hour=24 minute=0"):
        every_two_days_at(24, 0)


def test_every_two_days_at_even_uses_even_dom() -> None:
    cron, start = every_two_days_at(8, 0, days="even")
    assert cron == "0 8 2-30/2 * *"
    assert start == datetime(2026, 9, 27, 8, 0, tzinfo=ZoneInfo("America/Sao_Paulo"))


def test_every_two_days_at_rejects_unknown_days() -> None:
    with pytest.raises(ValueError, match=r"got 'weekly'"):
        every_two_days_at(8, 0, days="weekly")


def test_servico_grupo_runs_every_two_days_at_eight() -> None:
    src = (DAGS_DIR / "open_gov_servico_grupo.py").read_text(encoding="utf-8")
    assert "every_two_days_at(8, 0)" in src
    assert "paused=False" in src


CATSER_TWO_DAY_SLOTS = (
    ("servico_grupo", 8, 0),
    ("servico_item", 8, 15),
    ("servico_divisao", 8, 30),
    ("servico_classe", 9, 0),
    ("servico_natureza_despesa", 9, 15),
    ("servico_secao", 9, 30),
    ("servico_subclasse", 9, 45),
    ("servico_unidade_medida", 10, 0),
)


@pytest.mark.parametrize("script,hour,minute", CATSER_TWO_DAY_SLOTS)
def test_catser_dag_runs_every_two_days_at_slot(
    script: str, hour: int, minute: int
) -> None:
    src = (DAGS_DIR / f"open_gov_{script}.py").read_text(encoding="utf-8")
    assert f"every_two_days_at({hour}, {minute})" in src
    assert "paused=False" in src

from pathlib import Path

import pytest

DAGS_DIR = Path(__file__).resolve().parents[2] / "dags"

CONTRATACAO_SCRIPTS = (
    "contratacao",
    "contratacao_item",
    "contratacao_resultado",
)


@pytest.mark.parametrize("script", CONTRATACAO_SCRIPTS)
def test_contratacoes_dag_is_manual_airflow3_task(script: str) -> None:
    src = (DAGS_DIR / f"open_gov_{script}.py").read_text(encoding="utf-8")
    assert f'dag_id="open_gov_{script}"' in src
    assert "register_ingest_dag" in src
    assert f"etl.ingestion.contratacoes.{script}" in src
    assert 'tags=["open-gov", "contratacoes"]' in src
    # Airflow dag_discovery_safe_mode only parses files containing "airflow".
    assert "airflow" in src.lower()
    # Airflow loads the file without adding its directory to sys.path.
    assert "sys.path.insert(0, str(Path(__file__).resolve().parent))" in src

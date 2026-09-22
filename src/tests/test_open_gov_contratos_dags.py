from pathlib import Path

import pytest

DAGS_DIR = Path(__file__).resolve().parents[2] / "dags"

CONTRATO_SCRIPTS = (
    "contrato",
    "contrato_item",
    "contrato_fim_vigencia",
)


@pytest.mark.parametrize("script", CONTRATO_SCRIPTS)
def test_contratos_dag_is_manual_airflow3_task(script: str) -> None:
    src = (DAGS_DIR / f"open_gov_{script}.py").read_text(encoding="utf-8")
    assert f'dag_id="open_gov_{script}"' in src
    assert "register_ingest_dag" in src
    assert f"etl.ingestion.contratos.{script}" in src
    assert 'tags=["open-gov", "contratos"]' in src
    # Airflow dag_discovery_safe_mode only parses files containing "airflow".
    assert "airflow" in src.lower()
    # Airflow loads the file without adding its directory to sys.path.
    assert "sys.path.insert(0, str(Path(__file__).resolve().parent))" in src

from pathlib import Path

import pytest

DAGS_DIR = Path(__file__).resolve().parents[2] / "dags"
FACTORY = DAGS_DIR / "open_gov_ingest.py"

CATMAT_SCRIPTS = (
    "material_group",
    "material_class",
    "material_pdm",
    "material_item",
    "material_natureza_despesa",
    "material_unidade_fornecimento",
    "material_caracteristica",
)


def test_ingest_dag_factory_is_manual_airflow3() -> None:
    src = FACTORY.read_text(encoding="utf-8")
    assert "from airflow.sdk import dag, task" in src
    assert "schedule=None" in src
    assert "run_named_ingest" in src


@pytest.mark.parametrize("script", CATMAT_SCRIPTS)
def test_catmat_dag_is_manual_airflow3_task(script: str) -> None:
    src = (DAGS_DIR / f"open_gov_{script}.py").read_text(encoding="utf-8")
    assert f'dag_id="open_gov_{script}"' in src
    assert "register_ingest_dag" in src
    assert f"etl.ingestion.material.{script}" in src
    assert 'tags=["open-gov", "catmat"]' in src
    # Airflow dag_discovery_safe_mode only parses files containing "airflow".
    assert "airflow" in src.lower()
    # Airflow loads the file without adding its directory to sys.path.
    assert "sys.path.insert(0, str(Path(__file__).resolve().parent))" in src

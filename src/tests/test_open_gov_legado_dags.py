from pathlib import Path

import pytest

DAGS_DIR = Path(__file__).resolve().parents[2] / "dags"

LEGADO_SCRIPTS = (
    "legado_licitacao",
    "legado_item_licitacao",
    "legado_pregao",
    "legado_item_pregao",
    "legado_compra_sem_licitacao",
    "legado_item_sem_licitacao",
    "legado_rdc",
)


@pytest.mark.parametrize("script", LEGADO_SCRIPTS)
def test_legado_dag_is_manual_airflow3_task(script: str) -> None:
    src = (DAGS_DIR / f"open_gov_{script}.py").read_text(encoding="utf-8")
    assert f'dag_id="open_gov_{script}"' in src
    assert "register_ingest_dag" in src
    assert f"etl.ingestion.legado.{script}" in src
    assert 'tags=["open-gov", "legado"]' in src
    # Airflow dag_discovery_safe_mode only parses files containing "airflow".
    assert "airflow" in src.lower()
    # Airflow loads the file without adding its directory to sys.path.
    assert "sys.path.insert(0, str(Path(__file__).resolve().parent))" in src

from pathlib import Path

import pytest

DAGS_DIR = Path(__file__).resolve().parents[2] / "dags"

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

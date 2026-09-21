from pathlib import Path

DAGS_DIR = Path(__file__).resolve().parents[2] / "dags"
DAG_FILE = DAGS_DIR / "open_gov_preco_material.py"


def test_preco_material_dag_is_manual_airflow3_task() -> None:
    src = DAG_FILE.read_text(encoding="utf-8")
    assert 'dag_id="open_gov_preco_material"' in src
    assert "register_ingest_dag" in src
    assert "etl.ingestion.precos.preco_material" in src
    assert 'tags=["open-gov", "precos"]' in src

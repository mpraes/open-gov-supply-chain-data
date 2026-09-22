from pathlib import Path

DAGS_DIR = Path(__file__).resolve().parents[2] / "dags"
DAG_FILE = DAGS_DIR / "open_gov_ocds_release.py"


def test_ocds_release_dag_is_manual_airflow3_task() -> None:
    src = DAG_FILE.read_text(encoding="utf-8")
    assert 'dag_id="open_gov_ocds_release"' in src
    assert "register_ingest_dag" in src
    assert "etl.ingestion.ocds.ocds_release" in src
    assert 'tags=["open-gov", "ocds"]' in src
    # Airflow dag_discovery_safe_mode only parses files containing "airflow".
    assert "airflow" in src.lower()
    # Airflow loads the file without adding its directory to sys.path.
    assert "sys.path.insert(0, str(Path(__file__).resolve().parent))" in src

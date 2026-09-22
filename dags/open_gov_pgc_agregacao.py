# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_pgc_agregacao",
    module_path="etl.ingestion.planejamento.pgc_agregacao",
    tags=["open-gov", "planejamento"],
    task_id="ingest_pgc_agregacao",
    doc="Manual trigger for `3_consultarPgcAgregacao`.",
)

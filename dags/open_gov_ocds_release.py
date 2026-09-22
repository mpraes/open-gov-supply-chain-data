# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_ocds_release",
    module_path="etl.ingestion.ocds.ocds_release",
    tags=["open-gov", "ocds"],
    task_id="ingest_ocds_release",
    doc="Manual trigger for `1_releases`.",
)

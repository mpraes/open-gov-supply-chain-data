# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_arp_unidade_item",
    module_path="etl.ingestion.arp.arp_unidade_item",
    tags=["open-gov", "arp"],
    task_id="ingest_arp_unidade_item",
    doc="Manual trigger for `3_consultarUnidadesItem`.",
)

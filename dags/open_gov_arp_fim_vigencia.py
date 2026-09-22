# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_arp_fim_vigencia",
    module_path="etl.ingestion.arp.arp_fim_vigencia",
    tags=["open-gov", "arp"],
    task_id="ingest_arp_fim_vigencia",
    doc="Manual trigger for `1.2_consultarARP_FimVigencia`.",
)

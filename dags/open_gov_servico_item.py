# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_servico_item",
    module_path="etl.ingestion.servico.servico_item",
    tags=["open-gov", "catser"],
    task_id="ingest_servico_item",
    doc="Manual trigger for `6_consultarItemServico`.",
)

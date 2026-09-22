# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_contrato",
    module_path="etl.ingestion.contratos.contrato",
    tags=["open-gov", "contratos"],
    task_id="ingest_contrato",
    doc="Manual trigger for `1_consultarContratos`.",
)

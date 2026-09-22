# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_contratacao",
    module_path="etl.ingestion.contratacoes.contratacao",
    tags=["open-gov", "contratacoes"],
    task_id="ingest_contratacao",
    doc="Manual trigger for `1_consultarContratacoes_PNCP_14133`.",
)

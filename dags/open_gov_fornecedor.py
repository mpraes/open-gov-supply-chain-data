# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_fornecedor",
    module_path="etl.ingestion.fornecedor.fornecedor",
    tags=["open-gov", "fornecedor"],
    task_id="ingest_fornecedor",
    doc="Manual trigger for `1_consultarFornecedor`.",
)

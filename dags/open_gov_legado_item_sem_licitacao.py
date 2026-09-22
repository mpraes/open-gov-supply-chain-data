# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_legado_item_sem_licitacao",
    module_path="etl.ingestion.legado.legado_item_sem_licitacao",
    tags=["open-gov", "legado"],
    task_id="ingest_legado_item_sem_licitacao",
    doc="Manual trigger for `6_consultarCompraItensSemLicitacao`.",
)

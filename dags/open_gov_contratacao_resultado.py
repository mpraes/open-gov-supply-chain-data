# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_contratacao_resultado",
    module_path="etl.ingestion.contratacoes.contratacao_resultado",
    tags=["open-gov", "contratacoes"],
    task_id="ingest_contratacao_resultado",
    doc="Manual trigger for `3_consultarResultadoItensContratacoes_PNCP_14133`.",
)

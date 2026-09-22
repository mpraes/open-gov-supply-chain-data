# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_indicador_periodo",
    module_path="etl.ingestion.indicadores.indicador_periodo",
    tags=["open-gov", "indicadores"],
    task_id="ingest_indicador_periodo",
    doc="Manual trigger for `2_consultarIndicadoresPorPeriodo`.",
)

# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import every_two_days_at, register_ingest_dag

_SCHEDULE, _START = every_two_days_at(9, 15, days="even")

register_ingest_dag(
    dag_id="open_gov_material_natureza_despesa",
    module_path="etl.ingestion.material.material_natureza_despesa",
    tags=["open-gov", "catmat"],
    task_id="ingest_material_natureza_despesa",
    doc="Every even two days at 09:15 America/Sao_Paulo for `5_consultarMaterialNaturezaDespesa`.",
    schedule=_SCHEDULE,
    start_date=_START,
    paused=False,
)

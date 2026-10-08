# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import every_two_days_at, register_ingest_dag

_SCHEDULE, _START = every_two_days_at(9, 0, days="even")

register_ingest_dag(
    dag_id="open_gov_material_class",
    module_path="etl.ingestion.material.material_class",
    tags=["open-gov", "catmat"],
    task_id="ingest_material_class",
    doc="Every even two days at 09:00 America/Sao_Paulo for `2_consultarClasseMaterial`.",
    schedule=_SCHEDULE,
    start_date=_START,
    paused=False,
)

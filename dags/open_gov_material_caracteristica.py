# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import every_two_days_at, register_ingest_dag

_SCHEDULE, _START = every_two_days_at(9, 30, days="even")

register_ingest_dag(
    dag_id="open_gov_material_caracteristica",
    module_path="etl.ingestion.material.material_caracteristica",
    tags=["open-gov", "catmat"],
    task_id="ingest_material_caracteristica",
    doc="Every even two days at 09:30 America/Sao_Paulo for `7_consultarMaterialCaracteristicas`.",
    schedule=_SCHEDULE,
    start_date=_START,
    paused=False,
)

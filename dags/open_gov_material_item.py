# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import every_two_days_at, register_ingest_dag

_SCHEDULE, _START = every_two_days_at(8, 15, days="even")

register_ingest_dag(
    dag_id="open_gov_material_item",
    module_path="etl.ingestion.material.material_item",
    tags=["open-gov", "catmat"],
    task_id="ingest_material_item",
    doc="Every even two days at 08:15 America/Sao_Paulo for `4_consultarItemMaterial`.",
    schedule=_SCHEDULE,
    start_date=_START,
    paused=False,
)

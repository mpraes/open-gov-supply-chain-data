# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import every_two_days_at, register_ingest_dag

_SCHEDULE, _START = every_two_days_at(8, 15)

register_ingest_dag(
    dag_id="open_gov_servico_item",
    module_path="etl.ingestion.servico.servico_item",
    tags=["open-gov", "catser"],
    task_id="ingest_servico_item",
    doc="Every two days at 08:15 America/Sao_Paulo for `6_consultarItemServico`.",
    schedule=_SCHEDULE,
    start_date=_START,
    paused=False,
)

# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import every_two_days_at, register_ingest_dag

_SCHEDULE, _START = every_two_days_at(9, 45)

register_ingest_dag(
    dag_id="open_gov_servico_subclasse",
    module_path="etl.ingestion.servico.servico_subclasse",
    tags=["open-gov", "catser"],
    task_id="ingest_servico_subclasse",
    doc="Every two days at 09:45 America/Sao_Paulo for `5_consultarSubClasseServico`.",
    schedule=_SCHEDULE,
    start_date=_START,
    paused=False,
)

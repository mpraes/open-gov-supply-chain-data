# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import every_two_days_at, register_ingest_dag

_SCHEDULE, _START = every_two_days_at(8, 30)

register_ingest_dag(
    dag_id="open_gov_servico_divisao",
    module_path="etl.ingestion.servico.servico_divisao",
    tags=["open-gov", "catser"],
    task_id="ingest_servico_divisao",
    doc="Every two days at 08:30 America/Sao_Paulo for `2_consultarDivisaoServico`.",
    schedule=_SCHEDULE,
    start_date=_START,
    paused=False,
)

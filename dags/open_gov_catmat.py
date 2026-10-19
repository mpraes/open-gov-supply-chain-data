# airflow — dag_discovery_safe_mode only parses files containing this string
"""Registra a DAG de ingestão do CATMAT na ordem documentada."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_catalog import CATMAT_READY, CATMAT_STEPS
from open_gov_ingest import register_family_dag
from open_gov_schedule import every_two_days_at

_SCHEDULE, _START = every_two_days_at(8, 0, days="even")

register_family_dag(
    dag_id="open_gov_catmat",
    tags=["open-gov", "catmat"],
    doc="CATMAT in documented order. One API task at a time.",
    steps=CATMAT_STEPS,
    schedule=_SCHEDULE,
    start_date=_START,
    paused=False,
    outlet_asset=CATMAT_READY,
)

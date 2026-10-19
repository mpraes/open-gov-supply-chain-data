# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_catalog import LEGADO_STEPS
from open_gov_ingest import register_family_dag

register_family_dag(
    dag_id="open_gov_legado",
    tags=["open-gov", "legado"],
    doc="Lei 8.666 list dumps in series. Each script walks every year or slice.",
    steps=LEGADO_STEPS,
)

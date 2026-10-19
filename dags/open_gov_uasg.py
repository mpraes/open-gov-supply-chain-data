# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_catalog import UASG_STEPS
from open_gov_ingest import register_family_dag

register_family_dag(
    dag_id="open_gov_uasg",
    tags=["open-gov", "uasg"],
    doc="Órgão catalog, then UASG. Órgão emits the asset contratos and PGC read.",
    steps=UASG_STEPS,
)

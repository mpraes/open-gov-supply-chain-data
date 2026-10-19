# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_catalog import OCDS_STEPS, UASG_ORGAO_READY
from open_gov_ingest import register_family_dag

register_family_dag(
    dag_id="open_gov_ocds",
    tags=["open-gov", "ocds"],
    doc="OCDS releases for every 14-digit CNPJ in uasg_orgao.",
    steps=OCDS_STEPS,
    schedule_assets=(UASG_ORGAO_READY,),
    paused=False,
)

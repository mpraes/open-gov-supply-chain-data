# airflow — dag_discovery_safe_mode only parses files containing this string
"""Registra a DAG de ingestão de detalhe e agregação do PGC."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_catalog import PGC_STEPS, UASG_ORGAO_READY
from open_gov_ingest import register_family_dag

register_family_dag(
    dag_id="open_gov_pgc",
    tags=["open-gov", "planejamento"],
    doc="PGC detalhe and agregação for every órgão in uasg_orgao.",
    steps=PGC_STEPS,
    schedule_assets=(UASG_ORGAO_READY,),
    paused=False,
)

# airflow — dag_discovery_safe_mode only parses files containing this string
"""Registra a DAG de ingestão de contratos de cada órgão."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_catalog import CONTRATO_STEPS, UASG_ORGAO_READY
from open_gov_ingest import register_family_dag

register_family_dag(
    dag_id="open_gov_contratos",
    tags=["open-gov", "contratos"],
    doc="Contratos for every órgão in uasg_orgao.",
    steps=CONTRATO_STEPS,
    schedule_assets=(UASG_ORGAO_READY,),
    paused=False,
)

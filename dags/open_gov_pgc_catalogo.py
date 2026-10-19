# airflow — dag_discovery_safe_mode only parses files containing this string
"""Registra a DAG de ingestão do catálogo PGC após classes de material e grupos de serviço."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_catalog import MATERIAL_CLASS_READY, PGC_CATALOGO_STEPS, SERVICO_GRUPO_READY
from open_gov_ingest import register_family_dag

register_family_dag(
    dag_id="open_gov_pgc_catalogo",
    tags=["open-gov", "planejamento"],
    doc="PGC catálogo after material classes and serviço groups exist.",
    steps=PGC_CATALOGO_STEPS,
    schedule_assets=(MATERIAL_CLASS_READY, SERVICO_GRUPO_READY),
    paused=False,
)

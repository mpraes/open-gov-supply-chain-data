# airflow — dag_discovery_safe_mode only parses files containing this string
"""Registra a DAG de ingestão de indicadores consolidados e por período."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_catalog import INDICADOR_STEPS
from open_gov_ingest import register_family_dag

register_family_dag(
    dag_id="open_gov_indicadores",
    tags=["open-gov", "indicadores"],
    doc="Indicadores consolidados, then every year of the period endpoint.",
    steps=INDICADOR_STEPS,
)

# airflow — dag_discovery_safe_mode only parses files containing this string
"""Registra a DAG de ingestão de contratações, itens e resultados do PNCP."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_catalog import CONTRATACAO_STEPS
from open_gov_ingest import register_family_dag

register_family_dag(
    dag_id="open_gov_contratacoes",
    tags=["open-gov", "contratacoes"],
    doc="Contratações PNCP, then items and results, one task at a time.",
    steps=CONTRATACAO_STEPS,
)

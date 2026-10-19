# airflow — dag_discovery_safe_mode only parses files containing this string
"""Registra a DAG de ingestão de fornecedores ativos e inativos."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_catalog import FORNECEDOR_STEPS
from open_gov_ingest import register_family_dag

register_family_dag(
    dag_id="open_gov_fornecedor",
    tags=["open-gov", "fornecedor"],
    doc="Fornecedor ativo and inativo, one page at a time.",
    steps=FORNECEDOR_STEPS,
)

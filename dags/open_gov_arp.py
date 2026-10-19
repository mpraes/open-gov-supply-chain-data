# airflow — dag_discovery_safe_mode only parses files containing this string
"""Registra a DAG de ingestão de ARP, itens, empenhos, unidades e adesões."""
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_catalog import ARP_STEPS
from open_gov_ingest import register_family_dag

register_family_dag(
    dag_id="open_gov_arp",
    tags=["open-gov", "arp"],
    doc="ARP header first. Empenho reads arp. Unidade and adesão read arp_item.",
    steps=ARP_STEPS,
)

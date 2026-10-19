# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_catalog import CATMAT_READY, CATSER_READY, PRECO_STEPS
from open_gov_ingest import register_family_dag

register_family_dag(
    dag_id="open_gov_precos",
    tags=["open-gov", "precos"],
    doc="Practiced prices after CATMAT and CATSER catalogs are ready.",
    steps=PRECO_STEPS,
    schedule_assets=(CATMAT_READY, CATSER_READY),
    paused=False,
)

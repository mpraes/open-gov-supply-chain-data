# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_material_pdm",
    module_path="etl.ingestion.material.material_pdm",
    tags=["open-gov", "catmat"],
    task_id="ingest_material_pdm",
    doc="Manual trigger for `3_consultarPdmMaterial`.",
)

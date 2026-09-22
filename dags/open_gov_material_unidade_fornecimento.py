# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_material_unidade_fornecimento",
    module_path="etl.ingestion.material.material_unidade_fornecimento",
    tags=["open-gov", "catmat"],
    task_id="ingest_material_unidade_fornecimento",
    doc="Manual trigger for `6_consultarMaterialUnidadeFornecimento`.",
)

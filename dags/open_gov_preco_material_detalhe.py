# airflow — dag_discovery_safe_mode only parses files containing this string
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_preco_material_detalhe",
    module_path="etl.ingestion.precos.preco_material_detalhe",
    tags=["open-gov", "precos"],
    task_id="ingest_preco_material_detalhe",
    doc="Manual trigger for `2_consultarMaterialDetalhe`.",
)

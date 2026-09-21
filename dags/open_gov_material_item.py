from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_material_item",
    module_path="etl.ingestion.material.material_item",
    tags=["open-gov", "catmat"],
    task_id="ingest_material_item",
    doc="Manual trigger for `4_consultarItemMaterial`.",
)

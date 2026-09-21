from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_material_caracteristica",
    module_path="etl.ingestion.material.material_caracteristica",
    tags=["open-gov", "catmat"],
    task_id="ingest_material_caracteristica",
    doc="Manual trigger for `7_consultarMaterialCaracteristicas`.",
)

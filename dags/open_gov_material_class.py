from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_material_class",
    module_path="etl.ingestion.material.material_class",
    tags=["open-gov", "catmat"],
    task_id="ingest_material_class",
    doc="Manual trigger for `2_consultarClasseMaterial`.",
)

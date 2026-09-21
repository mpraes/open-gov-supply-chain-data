from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_material_group",
    module_path="etl.ingestion.material.material_group",
    tags=["open-gov", "catmat"],
    task_id="ingest_material_group",
    doc="Manual trigger for `1_consultarGrupoMaterial`.",
)

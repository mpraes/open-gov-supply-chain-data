from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_material_natureza_despesa",
    module_path="etl.ingestion.material.material_natureza_despesa",
    tags=["open-gov", "catmat"],
    task_id="ingest_material_natureza_despesa",
    doc="Manual trigger for `5_consultarMaterialNaturezaDespesa`.",
)

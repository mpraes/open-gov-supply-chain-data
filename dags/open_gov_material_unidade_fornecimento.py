from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_material_unidade_fornecimento",
    module_path="etl.ingestion.material.material_unidade_fornecimento",
    tags=["open-gov", "catmat"],
    task_id="ingest_material_unidade_fornecimento",
    doc="Manual trigger for `6_consultarMaterialUnidadeFornecimento`.",
)

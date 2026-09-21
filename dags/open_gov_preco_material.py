from open_gov_ingest import register_ingest_dag

register_ingest_dag(
    dag_id="open_gov_preco_material",
    module_path="etl.ingestion.precos.preco_material",
    tags=["open-gov", "precos"],
    task_id="ingest_preco_material",
    doc="Manual trigger for `1_consultarMaterial` practiced-price ingest.",
)

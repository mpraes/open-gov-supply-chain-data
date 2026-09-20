from typing import Any

from contracts.pgc_detalhe import PgcDetalheRecord
from config.load_secret_key import load_secret_key_func
from etl.ingestion.planejamento.map_pgc_fields import pgc_detalhe_fields
from etl.ingestion.planejamento.pgc_detalhe_sql import pgc_detalhe_upsert_sql
from etl.ingestion.planejamento.pgc_filters import pgc_ano
from etl.ingestion.planejamento.query_params import pgc_catalogo_query_params
from etl.ingestion.precos.batch_runner import run_preco_batch_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH

ENDPOINT_PATH = "/modulo-pgc/2_consultarPgcDetalheCatalogo"
PAGE_SIZE = 100
BATCH_SIZE = 20
TABLE_NAME = "pgc_detalhe_catalogo"
UPSERT_SQL = pgc_detalhe_upsert_sql(TABLE_NAME)


def map_pgc_detalhe_catalogo_row(row: dict[str, Any]) -> PgcDetalheRecord:
    """Map one consultarPgcDetalheCatalogo resultado object to PgcDetalheRecord.

    Example:
        record = map_pgc_detalhe_catalogo_row({"codigoUasg": "1", ...})
    """
    return PgcDetalheRecord(**pgc_detalhe_fields(row))


def main() -> None:
    ano = pgc_ano(DEFAULT_ENV_PATH, load_secret_key_func)
    _ingest_catalogo("Material", "material_class", "cod_classe", ano)
    _ingest_catalogo("Servico", "servico_grupo", "cod_grupo", ano)


def _ingest_catalogo(tipo: str, catalog_table: str, catalog_column: str, ano: int) -> int:
    job = f"pgc_detalhe_catalogo_{tipo.lower()}:{ano}"
    return run_preco_batch_ingestion(
        logger_name=job,
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_pgc_detalhe_catalogo_row,
        table_name=TABLE_NAME,
        catalog_table=catalog_table,
        catalog_column=catalog_column,
        params_for_code=lambda code: pgc_catalogo_query_params(code, tipo=tipo, ano=ano),
        absent_dest_table=TABLE_NAME,
        absent_dest_column=_catalogo_dest_column(tipo),
        absent_filters={"ano_artefato": ano},
        batch_size=BATCH_SIZE,
        job_name=job,
    )


def _catalogo_dest_column(tipo: str) -> str:
    if tipo == "Material":
        return "codigo_classe_material"
    if tipo == "Servico":
        return "codigo_grupo_servico"
    raise ValueError(f"tipo expected Material or Servico, got {tipo!r}")


if __name__ == "__main__":
    main()

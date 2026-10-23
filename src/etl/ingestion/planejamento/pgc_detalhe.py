"""Ingere consultarPgcDetalhe na tabela pgc_detalhe."""

from typing import Any

from contracts.pgc_detalhe import PgcDetalheRecord
from etl.ingestion.full_dump import for_each_dump_year
from etl.ingestion.orgao_catalog import read_buyer_cnpjs
from etl.ingestion.page_runner import run_page_batch_ingestion
from etl.ingestion.planejamento.map_pgc_fields import pgc_detalhe_fields
from etl.ingestion.planejamento.pgc_detalhe_sql import pgc_detalhe_upsert_sql
from etl.ingestion.planejamento.query_params import pgc_detalhe_query_params

ENDPOINT_PATH = "/modulo-pgc/1_consultarPgcDetalhe"
PAGE_SIZE = 100
TABLE_NAME = "pgc_detalhe"
UPSERT_SQL = pgc_detalhe_upsert_sql(TABLE_NAME)


def map_pgc_detalhe_row(row: dict[str, Any]) -> PgcDetalheRecord:
    """Mapeia um objeto resultado de consultarPgcDetalhe para PgcDetalheRecord.

    Exemplo:
        record = map_pgc_detalhe_row({"codigoUasg": "1", "orgao": "36000", ...})
    """
    return PgcDetalheRecord(**pgc_detalhe_fields(row))


def main() -> None:
    """Ingere consultarPgcDetalhe de cada CNPJ de uasg_orgao na tabela pgc_detalhe.

    Exemplo:
        main()
    """
    for cnpj in read_buyer_cnpjs():
        _ingest_cnpj(cnpj)


def _ingest_cnpj(cnpj: str) -> None:
    """Ingere consultarPgcDetalhe do CNPJ em cada ano do dump."""
    for_each_dump_year(lambda ano: _ingest_detalhe(cnpj, ano))


def _ingest_detalhe(cnpj: str, ano: int) -> None:
    """Ingere consultarPgcDetalhe do CNPJ e do ano na tabela pgc_detalhe."""
    run_page_batch_ingestion(
        logger_name="pgc_detalhe",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_pgc_detalhe_row,
        table_name=TABLE_NAME,
        query_params=pgc_detalhe_query_params(cnpj, ano),
        job_name=f"pgc_detalhe:{cnpj}:{ano}",
    )


if __name__ == "__main__":
    main()

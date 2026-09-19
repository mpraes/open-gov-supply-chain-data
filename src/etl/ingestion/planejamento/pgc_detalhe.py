from typing import Any

from contracts.pgc_detalhe import PgcDetalheRecord
from config.load_secret_key import load_secret_key_func
from etl.ingestion.page_runner import run_page_batch_ingestion
from etl.ingestion.planejamento.map_pgc_fields import pgc_detalhe_fields
from etl.ingestion.planejamento.pgc_detalhe_sql import pgc_detalhe_upsert_sql
from etl.ingestion.planejamento.pgc_filters import pgc_optional_uasg, pgc_orgao_ano
from etl.ingestion.planejamento.query_params import pgc_detalhe_query_params
from etl.ingestion.script_runner import DEFAULT_ENV_PATH

ENDPOINT_PATH = "/modulo-pgc/1_consultarPgcDetalhe"
PAGE_SIZE = 100
TABLE_NAME = "pgc_detalhe"
UPSERT_SQL = pgc_detalhe_upsert_sql(TABLE_NAME)


def map_pgc_detalhe_row(row: dict[str, Any]) -> PgcDetalheRecord:
    """Map one consultarPgcDetalhe resultado object to PgcDetalheRecord.

    Example:
        record = map_pgc_detalhe_row({"codigoUasg": "1", "orgao": "36000", ...})
    """
    return PgcDetalheRecord(**pgc_detalhe_fields(row))


def main() -> None:
    orgao, ano = pgc_orgao_ano(DEFAULT_ENV_PATH, load_secret_key_func)
    uasg = pgc_optional_uasg(DEFAULT_ENV_PATH, load_secret_key_func)
    run_page_batch_ingestion(
        logger_name="pgc_detalhe",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_pgc_detalhe_row,
        table_name=TABLE_NAME,
        query_params=pgc_detalhe_query_params(orgao, ano, uasg),
        job_name=f"pgc_detalhe:{orgao}:{ano}",
    )


if __name__ == "__main__":
    main()

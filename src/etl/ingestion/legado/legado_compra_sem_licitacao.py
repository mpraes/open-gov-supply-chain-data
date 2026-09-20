from typing import Any

from contracts.legado_compra_sem_licitacao import LegadoCompraSemLicitacaoRecord
from config.load_secret_key import load_secret_key_func
from etl.ingestion.legado.filters import legado_ano, legado_optional_uasg
from etl.ingestion.legado.legado_sql import legado_upsert_sql
from etl.ingestion.legado.map_legado_fields import legado_compra_sem_licitacao_fields
from etl.ingestion.legado.query_params import (
    legado_compra_sem_licitacao_query_params,
    legado_job_name,
)
from etl.ingestion.page_runner import run_page_batch_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH

ENDPOINT_PATH = "/modulo-legado/5_consultarComprasSemLicitacao"
PAGE_SIZE = 100
TABLE_NAME = "legado_compra_sem_licitacao"
UPSERT_SQL = legado_upsert_sql(TABLE_NAME)


def map_legado_compra_sem_licitacao_row(
    row: dict[str, Any],
) -> LegadoCompraSemLicitacaoRecord:
    """Map one consultarComprasSemLicitacao resultado object.

    Example:
        record = map_legado_compra_sem_licitacao_row({"id_compra": "d1"})
    """
    return LegadoCompraSemLicitacaoRecord(**legado_compra_sem_licitacao_fields(row))


def main() -> None:
    ano = legado_ano(DEFAULT_ENV_PATH, load_secret_key_func)
    uasg = legado_optional_uasg(DEFAULT_ENV_PATH, load_secret_key_func)
    run_page_batch_ingestion(
        logger_name="legado_compra_sem_licitacao",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_legado_compra_sem_licitacao_row,
        table_name=TABLE_NAME,
        query_params=legado_compra_sem_licitacao_query_params(ano, uasg),
        job_name=legado_job_name("legado_compra_sem_licitacao", ano, uasg),
    )


if __name__ == "__main__":
    main()

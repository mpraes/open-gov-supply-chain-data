from typing import Any

from contracts.legado_item_licitacao import LegadoItemLicitacaoRecord
from config.load_secret_key import load_secret_key_func
from etl.ingestion.legado.filters import legado_modalidade, legado_optional_uasg
from etl.ingestion.legado.legado_sql import legado_upsert_sql
from etl.ingestion.legado.map_legado_fields import legado_item_licitacao_fields
from etl.ingestion.legado.query_params import (
    legado_item_licitacao_query_params,
    legado_job_name,
)
from etl.ingestion.page_runner import run_page_batch_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH

ENDPOINT_PATH = "/modulo-legado/2_consultarItemLicitacao"
PAGE_SIZE = 100
TABLE_NAME = "legado_item_licitacao"
UPSERT_SQL = legado_upsert_sql(TABLE_NAME)


def map_legado_item_licitacao_row(row: dict[str, Any]) -> LegadoItemLicitacaoRecord:
    """Map one consultarItemLicitacao resultado object.

    Example:
        record = map_legado_item_licitacao_row({"id_compra": "c1", "id_compra_item": "i1"})
    """
    return LegadoItemLicitacaoRecord(**legado_item_licitacao_fields(row))


def main() -> None:
    modalidade = legado_modalidade(DEFAULT_ENV_PATH, load_secret_key_func)
    uasg = legado_optional_uasg(DEFAULT_ENV_PATH, load_secret_key_func)
    run_page_batch_ingestion(
        logger_name="legado_item_licitacao",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_legado_item_licitacao_row,
        table_name=TABLE_NAME,
        query_params=legado_item_licitacao_query_params(modalidade, uasg),
        job_name=legado_job_name("legado_item_licitacao", modalidade, uasg),
    )


if __name__ == "__main__":
    main()

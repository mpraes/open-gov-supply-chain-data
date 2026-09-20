from typing import Any

from contracts.legado_licitacao import LegadoLicitacaoRecord
from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_watermark import DateWatermark
from etl.ingestion.legado.filters import legado_date_range, legado_optional_uasg
from etl.ingestion.legado.legado_sql import legado_upsert_sql
from etl.ingestion.legado.map_legado_fields import legado_licitacao_fields
from etl.ingestion.legado.query_params import legado_job_name, legado_licitacao_query_params
from etl.ingestion.page_runner import run_page_batch_ingestion
from etl.ingestion.script_runner import DEFAULT_ENV_PATH

ENDPOINT_PATH = "/modulo-legado/1_consultarLicitacao"
PAGE_SIZE = 100
TABLE_NAME = "legado_licitacao"
UPSERT_SQL = legado_upsert_sql(TABLE_NAME)


def map_legado_licitacao_row(row: dict[str, Any]) -> LegadoLicitacaoRecord:
    """Map one consultarLicitacao resultado object.

    Example:
        record = map_legado_licitacao_row({"id_compra": "123", "objeto": "x"})
    """
    return LegadoLicitacaoRecord(**legado_licitacao_fields(row))


def main() -> None:
    inicial, final = legado_date_range(DEFAULT_ENV_PATH, load_secret_key_func)
    uasg = legado_optional_uasg(DEFAULT_ENV_PATH, load_secret_key_func)
    run_page_batch_ingestion(
        logger_name="legado_licitacao",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_legado_licitacao_row,
        table_name=TABLE_NAME,
        query_params=legado_licitacao_query_params(inicial, final, uasg),
        job_name=legado_job_name("legado_licitacao", inicial, final, uasg),
        date_watermark=DateWatermark(
            table=TABLE_NAME,
            column="data_publicacao",
            start_param="data_publicacao_inicial",
            end_param="data_publicacao_final",
            where=None if uasg is None else {"uasg": uasg},
        ),
    )


if __name__ == "__main__":
    main()

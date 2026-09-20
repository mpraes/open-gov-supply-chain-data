from typing import Any

from contracts.pgc_agregacao import PgcAgregacaoRecord
from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_schema import dest_table
from etl.ingestion.page_runner import run_page_batch_ingestion
from etl.ingestion.planejamento.map_pgc_fields import pgc_agregacao_fields
from etl.ingestion.planejamento.pgc_filters import pgc_orgao_ano
from etl.ingestion.planejamento.query_params import pgc_agregacao_query_params
from etl.ingestion.script_runner import DEFAULT_ENV_PATH

ENDPOINT_PATH = "/modulo-pgc/3_consultarPgcAgregacao"
PAGE_SIZE: int | None = None
TABLE_NAME = "pgc_agregacao"

UPSERT_SQL = f"""
INSERT INTO {dest_table("pgc_agregacao")} (
    orgao, ano, poder, esfera, data_hora_publicacao_pncp,
    data_hora_atualizacao, quantidade_total_itens, valor_total_estimado
)
VALUES (
    %(orgao)s, %(ano)s, %(poder)s, %(esfera)s, %(data_hora_publicacao_pncp)s,
    %(data_hora_atualizacao)s, %(quantidade_total_itens)s, %(valor_total_estimado)s
)
ON CONFLICT (orgao, ano) DO UPDATE SET
poder = EXCLUDED.poder,
esfera = EXCLUDED.esfera,
data_hora_publicacao_pncp = EXCLUDED.data_hora_publicacao_pncp,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
quantidade_total_itens = EXCLUDED.quantidade_total_itens,
valor_total_estimado = EXCLUDED.valor_total_estimado,
data_hora_carga = now();
"""


def map_pgc_agregacao_row(row: dict[str, Any]) -> PgcAgregacaoRecord:
    """Map one consultarPgcAgregacao resultado object to PgcAgregacaoRecord.

    Example:
        record = map_pgc_agregacao_row({"orgao": "36000", "ano": 2026})
    """
    return PgcAgregacaoRecord(**pgc_agregacao_fields(row))


def main() -> None:
    orgao, ano = pgc_orgao_ano(DEFAULT_ENV_PATH, load_secret_key_func)
    run_page_batch_ingestion(
        logger_name="pgc_agregacao",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_pgc_agregacao_row,
        table_name=TABLE_NAME,
        query_params=pgc_agregacao_query_params(orgao, ano),
        job_name=f"pgc_agregacao:{orgao}:{ano}",
    )


if __name__ == "__main__":
    main()

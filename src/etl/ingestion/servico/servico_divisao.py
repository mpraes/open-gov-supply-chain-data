from typing import Any

from contracts.servico_divisao import ServicoDivisaoRecord
from etl.ingestion.dest_schema import dest_table
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-servico/2_consultarDivisaoServico"
PAGE_SIZE: int | None = None

UPSERT_SQL = f"""
INSERT INTO {dest_table("servico_divisao")} (
    cod_divisao, cod_secao, nome_secao, nome_divisao, status_divisao, data_hora_atualizacao
)
VALUES (
    %(cod_divisao)s, %(cod_secao)s, %(nome_secao)s, %(nome_divisao)s,
    %(status_divisao)s, %(data_hora_atualizacao)s
)
ON CONFLICT (cod_divisao) DO UPDATE SET
cod_secao = EXCLUDED.cod_secao,
nome_secao = EXCLUDED.nome_secao,
nome_divisao = EXCLUDED.nome_divisao,
status_divisao = EXCLUDED.status_divisao,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
data_hora_carga = now();
"""


def map_servico_divisao_row(row: dict[str, Any]) -> ServicoDivisaoRecord:
    """Map one API resultado object to ServicoDivisaoRecord.

    Example:
        record = map_servico_divisao_row({"codigoDivisao": 2, "codigoSecao": 1, ...})
    """
    return ServicoDivisaoRecord(
        cod_divisao=row["codigoDivisao"],
        cod_secao=row["codigoSecao"],
        nome_secao=row["nomeSecao"],
        nome_divisao=row["nomeDivisao"],
        status_divisao=row["statusDivisao"],
        data_hora_atualizacao=row["dataHoraAtualizacao"],
    )


def main() -> None:
    run_page_batch_ingestion(
        logger_name="servico_divisao",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_servico_divisao_row,
        table_name="servico_divisao",
    )


if __name__ == "__main__":
    main()

from typing import Any

from contracts.uasg import UasgRecord
from etl.ingestion.page_runner import run_page_batch_ingestion
from etl.ingestion.uasg.map_uasg_fields import uasg_fields
from etl.ingestion.uasg.query_params import uasg_job_name, uasg_query_params

ENDPOINT_PATH = "/modulo-uasg/1_consultarUasg"
PAGE_SIZE: int | None = None
TABLE_NAME = "uasg"

UPSERT_SQL = """
INSERT INTO uasg (
    codigo_uasg, nome_uasg, uso_sisg, adesao_siasg, sigla_uf,
    codigo_municipio, codigo_municipio_ibge, nome_municipio_ibge,
    codigo_unidade_polo, nome_unidade_polo, codigo_unidade_espelho,
    nome_unidade_espelho, uasg_cadastradora, cnpj_cpf_uasg, codigo_orgao,
    cnpj_cpf_orgao, cnpj_cpf_orgao_vinculado, cnpj_cpf_orgao_superior,
    codigo_siorg, status_uasg, data_implantacao_sidec, data_hora_movimento
)
VALUES (
    %(codigo_uasg)s, %(nome_uasg)s, %(uso_sisg)s, %(adesao_siasg)s, %(sigla_uf)s,
    %(codigo_municipio)s, %(codigo_municipio_ibge)s, %(nome_municipio_ibge)s,
    %(codigo_unidade_polo)s, %(nome_unidade_polo)s, %(codigo_unidade_espelho)s,
    %(nome_unidade_espelho)s, %(uasg_cadastradora)s, %(cnpj_cpf_uasg)s,
    %(codigo_orgao)s, %(cnpj_cpf_orgao)s, %(cnpj_cpf_orgao_vinculado)s,
    %(cnpj_cpf_orgao_superior)s, %(codigo_siorg)s, %(status_uasg)s,
    %(data_implantacao_sidec)s, %(data_hora_movimento)s
)
ON CONFLICT (codigo_uasg) DO UPDATE SET
nome_uasg = EXCLUDED.nome_uasg,
uso_sisg = EXCLUDED.uso_sisg,
adesao_siasg = EXCLUDED.adesao_siasg,
sigla_uf = EXCLUDED.sigla_uf,
codigo_municipio = EXCLUDED.codigo_municipio,
codigo_municipio_ibge = EXCLUDED.codigo_municipio_ibge,
nome_municipio_ibge = EXCLUDED.nome_municipio_ibge,
codigo_unidade_polo = EXCLUDED.codigo_unidade_polo,
nome_unidade_polo = EXCLUDED.nome_unidade_polo,
codigo_unidade_espelho = EXCLUDED.codigo_unidade_espelho,
nome_unidade_espelho = EXCLUDED.nome_unidade_espelho,
uasg_cadastradora = EXCLUDED.uasg_cadastradora,
cnpj_cpf_uasg = EXCLUDED.cnpj_cpf_uasg,
codigo_orgao = EXCLUDED.codigo_orgao,
cnpj_cpf_orgao = EXCLUDED.cnpj_cpf_orgao,
cnpj_cpf_orgao_vinculado = EXCLUDED.cnpj_cpf_orgao_vinculado,
cnpj_cpf_orgao_superior = EXCLUDED.cnpj_cpf_orgao_superior,
codigo_siorg = EXCLUDED.codigo_siorg,
status_uasg = EXCLUDED.status_uasg,
data_implantacao_sidec = EXCLUDED.data_implantacao_sidec,
data_hora_movimento = EXCLUDED.data_hora_movimento,
data_hora_carga = now();
"""


def map_uasg_row(row: dict[str, Any]) -> UasgRecord:
    """Map one consultarUasg resultado object to UasgRecord.

    Example:
        record = map_uasg_row({"codigoUasg": "153001", "nomeUasg": "x", ...})
    """
    return UasgRecord(**uasg_fields(row))


def main() -> None:
    for status in (True, False):
        run_page_batch_ingestion(
            logger_name="uasg",
            endpoint_path=ENDPOINT_PATH,
            page_size=PAGE_SIZE,
            upsert_sql=UPSERT_SQL,
            map_row=map_uasg_row,
            table_name=TABLE_NAME,
            query_params=uasg_query_params(status),
            job_name=uasg_job_name(status),
        )


if __name__ == "__main__":
    main()

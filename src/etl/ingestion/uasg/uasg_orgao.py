from typing import Any

from contracts.uasg_orgao import UasgOrgaoRecord
from etl.ingestion.dest_schema import dest_table
from etl.ingestion.page_runner import run_page_batch_ingestion
from etl.ingestion.uasg.map_uasg_fields import uasg_orgao_fields
from etl.ingestion.uasg.query_params import uasg_orgao_job_name, uasg_orgao_query_params

ENDPOINT_PATH = "/modulo-uasg/2_consultarOrgao"
PAGE_SIZE: int | None = None
TABLE_NAME = "uasg_orgao"

UPSERT_SQL = f"""
INSERT INTO {dest_table("uasg_orgao")} (
    codigo_orgao, nome_orgao, nome_mnemonico_orgao, cnpj_cpf_orgao,
    codigo_orgao_vinculado, cnpj_cpf_orgao_vinculado, nome_orgao_vinculado,
    codigo_orgao_superior, cnpj_cpf_orgao_superior, nome_orgao_superior,
    codigo_tipo_administracao, nome_tipo_administracao, poder, esfera,
    uso_sisg, status_orgao, data_hora_movimento
)
VALUES (
    %(codigo_orgao)s, %(nome_orgao)s, %(nome_mnemonico_orgao)s, %(cnpj_cpf_orgao)s,
    %(codigo_orgao_vinculado)s, %(cnpj_cpf_orgao_vinculado)s,
    %(nome_orgao_vinculado)s, %(codigo_orgao_superior)s,
    %(cnpj_cpf_orgao_superior)s, %(nome_orgao_superior)s,
    %(codigo_tipo_administracao)s, %(nome_tipo_administracao)s, %(poder)s,
    %(esfera)s, %(uso_sisg)s, %(status_orgao)s, %(data_hora_movimento)s
)
ON CONFLICT (codigo_orgao) DO UPDATE SET
nome_orgao = EXCLUDED.nome_orgao,
nome_mnemonico_orgao = EXCLUDED.nome_mnemonico_orgao,
cnpj_cpf_orgao = EXCLUDED.cnpj_cpf_orgao,
codigo_orgao_vinculado = EXCLUDED.codigo_orgao_vinculado,
cnpj_cpf_orgao_vinculado = EXCLUDED.cnpj_cpf_orgao_vinculado,
nome_orgao_vinculado = EXCLUDED.nome_orgao_vinculado,
codigo_orgao_superior = EXCLUDED.codigo_orgao_superior,
cnpj_cpf_orgao_superior = EXCLUDED.cnpj_cpf_orgao_superior,
nome_orgao_superior = EXCLUDED.nome_orgao_superior,
codigo_tipo_administracao = EXCLUDED.codigo_tipo_administracao,
nome_tipo_administracao = EXCLUDED.nome_tipo_administracao,
poder = EXCLUDED.poder,
esfera = EXCLUDED.esfera,
uso_sisg = EXCLUDED.uso_sisg,
status_orgao = EXCLUDED.status_orgao,
data_hora_movimento = EXCLUDED.data_hora_movimento,
data_hora_carga = now();
"""


def map_uasg_orgao_row(row: dict[str, Any]) -> UasgOrgaoRecord:
    """Map one consultarOrgao resultado object to UasgOrgaoRecord.

    Example:
        record = map_uasg_orgao_row({"codigoOrgao": 36000, "nomeOrgao": "x", ...})
    """
    return UasgOrgaoRecord(**uasg_orgao_fields(row))


def main() -> None:
    for status in (True, False):
        run_page_batch_ingestion(
            logger_name="uasg_orgao",
            endpoint_path=ENDPOINT_PATH,
            page_size=PAGE_SIZE,
            upsert_sql=UPSERT_SQL,
            map_row=map_uasg_orgao_row,
            table_name=TABLE_NAME,
            query_params=uasg_orgao_query_params(status),
            job_name=uasg_orgao_job_name(status),
        )


if __name__ == "__main__":
    main()

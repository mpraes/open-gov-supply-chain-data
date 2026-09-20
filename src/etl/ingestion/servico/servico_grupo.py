from typing import Any

from contracts.servico_grupo import ServicoGrupoRecord
from etl.ingestion.dest_schema import dest_table
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-servico/3_consultarGrupoServico"
PAGE_SIZE: int | None = None

UPSERT_SQL = f"""
INSERT INTO {dest_table("servico_grupo")} (
    cod_grupo, cod_divisao, nome_secao, nome_divisao, nome_grupo,
    status_grupo, data_hora_atualizacao
)
VALUES (
    %(cod_grupo)s, %(cod_divisao)s, %(nome_secao)s, %(nome_divisao)s, %(nome_grupo)s,
    %(status_grupo)s, %(data_hora_atualizacao)s
)
ON CONFLICT (cod_grupo) DO UPDATE SET
cod_divisao = EXCLUDED.cod_divisao,
nome_secao = EXCLUDED.nome_secao,
nome_divisao = EXCLUDED.nome_divisao,
nome_grupo = EXCLUDED.nome_grupo,
status_grupo = EXCLUDED.status_grupo,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
data_hora_carga = now();
"""


def map_servico_grupo_row(row: dict[str, Any]) -> ServicoGrupoRecord:
    """Map one API resultado object to ServicoGrupoRecord.

    Example:
        record = map_servico_grupo_row({"codigoGrupo": 3, "codigoDivisao": 2, ...})
    """
    return ServicoGrupoRecord(
        cod_grupo=row["codigoGrupo"],
        cod_divisao=row["codigoDivisao"],
        nome_secao=row["nomeSecao"],
        nome_divisao=row["nomeDivisao"],
        nome_grupo=row["nomeGrupo"],
        status_grupo=row["statusGrupo"],
        data_hora_atualizacao=row["dataHoraAtualizacao"],
    )


def main() -> None:
    run_page_batch_ingestion(
        logger_name="servico_grupo",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_servico_grupo_row,
        table_name="servico_grupo",
    )


if __name__ == "__main__":
    main()

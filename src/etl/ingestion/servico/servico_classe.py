from typing import Any

from contracts.servico_classe import ServicoClasseRecord
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-servico/4_consultarClasseServico"
PAGE_SIZE: int | None = None

UPSERT_SQL = """
INSERT INTO servico_classe (
    cod_classe, cod_grupo, nome_grupo, nome_classe, status_classe, data_hora_atualizacao
)
VALUES (
    %(cod_classe)s, %(cod_grupo)s, %(nome_grupo)s, %(nome_classe)s,
    %(status_classe)s, %(data_hora_atualizacao)s
)
ON CONFLICT (cod_classe) DO UPDATE SET
cod_grupo = EXCLUDED.cod_grupo,
nome_grupo = EXCLUDED.nome_grupo,
nome_classe = EXCLUDED.nome_classe,
status_classe = EXCLUDED.status_classe,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
data_hora_carga = now();
"""


def map_servico_classe_row(row: dict[str, Any]) -> ServicoClasseRecord:
    """Map one API resultado object to ServicoClasseRecord.

    Example:
        record = map_servico_classe_row({"codigoClasse": 4, "codigoGrupo": 3, ...})

    API docs name the status field `statusGrupo` on this endpoint; we store it as
    status_classe.
    """
    return ServicoClasseRecord(
        cod_classe=row["codigoClasse"],
        cod_grupo=row["codigoGrupo"],
        nome_grupo=row["nomeGrupo"],
        nome_classe=row["nomeClasse"],
        status_classe=row["statusGrupo"],
        data_hora_atualizacao=row["dataHoraAtualizacao"],
    )


def main() -> None:
    run_page_batch_ingestion(
        logger_name="servico_classe",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_servico_classe_row,
        table_name="servico_classe",
    )


if __name__ == "__main__":
    main()

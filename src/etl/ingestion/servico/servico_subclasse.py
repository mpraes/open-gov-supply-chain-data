from typing import Any

from contracts.servico_subclasse import ServicoSubclasseRecord
from etl.ingestion.dest_schema import dest_table
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-servico/5_consultarSubClasseServico"
PAGE_SIZE: int | None = None

UPSERT_SQL = f"""
INSERT INTO {dest_table("servico_subclasse")} (
    cod_subclasse, cod_classe, nome_classe, nome_subclasse,
    status_subclasse, data_hora_atualizacao
)
VALUES (
    %(cod_subclasse)s, %(cod_classe)s, %(nome_classe)s, %(nome_subclasse)s,
    %(status_subclasse)s, %(data_hora_atualizacao)s
)
ON CONFLICT (cod_subclasse) DO UPDATE SET
cod_classe = EXCLUDED.cod_classe,
nome_classe = EXCLUDED.nome_classe,
nome_subclasse = EXCLUDED.nome_subclasse,
status_subclasse = EXCLUDED.status_subclasse,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
data_hora_carga = now();
"""


def map_servico_subclasse_row(row: dict[str, Any]) -> ServicoSubclasseRecord:
    """Map one API resultado object to ServicoSubclasseRecord.

    Example:
        record = map_servico_subclasse_row({"codigoSubclasse": 5, ...})
    """
    return ServicoSubclasseRecord(
        cod_subclasse=row["codigoSubclasse"],
        cod_classe=row["codigoClasse"],
        nome_classe=row["nomeClasse"],
        nome_subclasse=row["nomeSubclasse"],
        status_subclasse=row["statusSubclasse"],
        data_hora_atualizacao=row["dataHoraAtualizacao"],
    )


def main() -> None:
    run_page_batch_ingestion(
        logger_name="servico_subclasse",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_servico_subclasse_row,
        table_name="servico_subclasse",
    )


if __name__ == "__main__":
    main()

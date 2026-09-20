from typing import Any

from contracts.servico_item import ServicoItemRecord
from etl.ingestion.dest_schema import dest_table
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-servico/6_consultarItemServico"
PAGE_SIZE = 500

UPSERT_SQL = f"""
INSERT INTO {dest_table("servico_item")} (
    cod_servico, cod_secao, nome_secao, cod_divisao, nome_divisao,
    cod_grupo, nome_grupo, cod_classe, nome_classe, cod_subclasse, nome_subclasse,
    nome_servico, cod_cpc, exclusivo_central_compras, status_servico,
    data_hora_atualizacao
)
VALUES (
    %(cod_servico)s, %(cod_secao)s, %(nome_secao)s, %(cod_divisao)s, %(nome_divisao)s,
    %(cod_grupo)s, %(nome_grupo)s, %(cod_classe)s, %(nome_classe)s,
    %(cod_subclasse)s, %(nome_subclasse)s, %(nome_servico)s, %(cod_cpc)s,
    %(exclusivo_central_compras)s, %(status_servico)s, %(data_hora_atualizacao)s
)
ON CONFLICT (cod_servico) DO UPDATE SET
cod_secao = EXCLUDED.cod_secao,
nome_secao = EXCLUDED.nome_secao,
cod_divisao = EXCLUDED.cod_divisao,
nome_divisao = EXCLUDED.nome_divisao,
cod_grupo = EXCLUDED.cod_grupo,
nome_grupo = EXCLUDED.nome_grupo,
cod_classe = EXCLUDED.cod_classe,
nome_classe = EXCLUDED.nome_classe,
cod_subclasse = EXCLUDED.cod_subclasse,
nome_subclasse = EXCLUDED.nome_subclasse,
nome_servico = EXCLUDED.nome_servico,
cod_cpc = EXCLUDED.cod_cpc,
exclusivo_central_compras = EXCLUDED.exclusivo_central_compras,
status_servico = EXCLUDED.status_servico,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
data_hora_carga = now();
"""


def map_servico_item_row(row: dict[str, Any]) -> ServicoItemRecord:
    """Map one API resultado object to ServicoItemRecord.

    Example:
        record = map_servico_item_row({"codigoServico": 100, ...})
    """
    return ServicoItemRecord(
        cod_servico=row["codigoServico"],
        cod_secao=row["codigoSecao"],
        nome_secao=row["nomeSecao"],
        cod_divisao=row["codigoDivisao"],
        nome_divisao=row["nomeDivisao"],
        cod_grupo=row["codigoGrupo"],
        nome_grupo=row["nomeGrupo"],
        cod_classe=row["codigoClasse"],
        nome_classe=row["nomeClasse"],
        cod_subclasse=row["codigoSubclasse"],
        nome_subclasse=row["nomeSubclasse"],
        nome_servico=row["nomeServico"],
        cod_cpc=row["codigoCpc"],
        exclusivo_central_compras=row["exclusivoCentralCompras"],
        status_servico=row["statusServico"],
        data_hora_atualizacao=row["dataHoraAtualizacao"],
    )


def main() -> None:
    run_page_batch_ingestion(
        logger_name="servico_item",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_servico_item_row,
        table_name="servico_item",
    )


if __name__ == "__main__":
    main()

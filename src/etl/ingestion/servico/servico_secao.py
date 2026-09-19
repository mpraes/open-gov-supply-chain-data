from typing import Any

from contracts.servico_secao import ServicoSecaoRecord
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-servico/1_consultarSecaoServico"
PAGE_SIZE: int | None = None

UPSERT_SQL = """
INSERT INTO servico_secao (cod_secao, nome_secao, status_secao, data_hora_atualizacao)
VALUES (%(cod_secao)s, %(nome_secao)s, %(status_secao)s, %(data_hora_atualizacao)s)
ON CONFLICT (cod_secao) DO UPDATE SET
nome_secao = EXCLUDED.nome_secao,
status_secao = EXCLUDED.status_secao,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
data_hora_carga = now();
"""


def map_servico_secao_row(row: dict[str, Any]) -> ServicoSecaoRecord:
    """Map one API resultado object to ServicoSecaoRecord.

    Example:
        record = map_servico_secao_row({"codigoSecao": 1, "nomeSecao": "x", ...})
    """
    return ServicoSecaoRecord(
        cod_secao=row["codigoSecao"],
        nome_secao=row["nomeSecao"],
        status_secao=row["statusSecao"],
        data_hora_atualizacao=row["dataHoraAtualizacao"],
    )


def main() -> None:
    run_page_batch_ingestion(
        logger_name="servico_secao",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_servico_secao_row,
        table_name="servico_secao",
    )


if __name__ == "__main__":
    main()

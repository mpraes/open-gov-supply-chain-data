from typing import Any

from contracts.servico_unidade_medida import ServicoUnidadeMedidaRecord
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-servico/7_consultarUndMedidaServico"
PAGE_SIZE: int | None = None

UPSERT_SQL = """
INSERT INTO servico_unidade_medida (
    cod_servico, sigla_unidade_medida, nome_unidade_medida, status_unidade_medida
)
VALUES (
    %(cod_servico)s, %(sigla_unidade_medida)s, %(nome_unidade_medida)s,
    %(status_unidade_medida)s
)
ON CONFLICT (cod_servico, sigla_unidade_medida) DO UPDATE SET
nome_unidade_medida = EXCLUDED.nome_unidade_medida,
status_unidade_medida = EXCLUDED.status_unidade_medida,
data_hora_carga = now();
"""


def map_servico_unidade_medida_row(row: dict[str, Any]) -> ServicoUnidadeMedidaRecord:
    """Map one API resultado object to ServicoUnidadeMedidaRecord.

    Example:
        record = map_servico_unidade_medida_row({"codigoServico": 100, ...})
    """
    return ServicoUnidadeMedidaRecord(
        cod_servico=row["codigoServico"],
        sigla_unidade_medida=row["siglaUnidadeMedida"],
        nome_unidade_medida=row["nomeUnidadeMedida"],
        status_unidade_medida=row["statusUnidadeMedida"],
    )


def main() -> None:
    run_page_batch_ingestion(
        logger_name="servico_unidade_medida",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_servico_unidade_medida_row,
        table_name="servico_unidade_medida",
    )


if __name__ == "__main__":
    main()

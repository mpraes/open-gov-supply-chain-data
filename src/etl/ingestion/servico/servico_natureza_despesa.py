from typing import Any

from contracts.servico_natureza_despesa import ServicoNaturezaDespesaRecord
from etl.ingestion.dest_schema import dest_table
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-servico/8_consultarNaturezaDespesaServico"
PAGE_SIZE: int | None = None

UPSERT_SQL = f"""
INSERT INTO {dest_table("servico_natureza_despesa")} (
    cod_servico, cod_natureza_despesa, nome_natureza_despesa, status_natureza_despesa
)
VALUES (
    %(cod_servico)s, %(cod_natureza_despesa)s, %(nome_natureza_despesa)s,
    %(status_natureza_despesa)s
)
ON CONFLICT (cod_servico, cod_natureza_despesa) DO UPDATE SET
nome_natureza_despesa = EXCLUDED.nome_natureza_despesa,
status_natureza_despesa = EXCLUDED.status_natureza_despesa,
data_hora_carga = now();
"""


def map_servico_natureza_despesa_row(row: dict[str, Any]) -> ServicoNaturezaDespesaRecord:
    """Map one API resultado object to ServicoNaturezaDespesaRecord.

    Example:
        record = map_servico_natureza_despesa_row({"codigoServico": 100, ...})
    """
    return ServicoNaturezaDespesaRecord(
        cod_servico=row["codigoServico"],
        cod_natureza_despesa=row["codigoNaturezaDespesa"],
        nome_natureza_despesa=row["nomeNaturezaDespesa"],
        status_natureza_despesa=row["statusNaturezaDespesa"],
    )


def main() -> None:
    run_page_batch_ingestion(
        logger_name="servico_natureza_despesa",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_servico_natureza_despesa_row,
        table_name="servico_natureza_despesa",
    )


if __name__ == "__main__":
    main()

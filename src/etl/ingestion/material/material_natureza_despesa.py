from typing import Any

from contracts.material_natureza_despesa import MaterialNaturezaDespesaRecord
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-material/5_consultarMaterialNaturezaDespesa"
PAGE_SIZE = 500

UPSERT_SQL = """
INSERT INTO material_natureza_despesa (
    cod_pdm, cod_natureza_despesa, nome_natureza_despesa, status_natureza_despesa
)
VALUES (
    %(cod_pdm)s, %(cod_natureza_despesa)s, %(nome_natureza_despesa)s,
    %(status_natureza_despesa)s
)
ON CONFLICT (cod_pdm, cod_natureza_despesa) DO UPDATE SET
nome_natureza_despesa = EXCLUDED.nome_natureza_despesa,
status_natureza_despesa = EXCLUDED.status_natureza_despesa,
data_hora_carga = now();
"""


def map_material_natureza_despesa_row(row: dict[str, Any]) -> MaterialNaturezaDespesaRecord:
    """Map one API resultado object to MaterialNaturezaDespesaRecord.

    Example:
        record = map_material_natureza_despesa_row({"codigoPdm": 1, ...})
    """
    return MaterialNaturezaDespesaRecord(
        cod_pdm=row["codigoPdm"],
        cod_natureza_despesa=row["codigoNaturezaDespesa"],
        nome_natureza_despesa=row["nomeNaturezaDespesa"],
        status_natureza_despesa=row["statusNaturezaDespesa"],
    )


def main() -> None:
    run_page_batch_ingestion(
        logger_name="material_natureza_despesa",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_material_natureza_despesa_row,
        table_name="material_natureza_despesa",
    )


if __name__ == "__main__":
    main()

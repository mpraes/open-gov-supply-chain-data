from typing import Any

from contracts.material_pdm import MaterialPdmRecord
from etl.ingestion.page_runner import run_page_batch_ingestion

ENDPOINT_PATH = "/modulo-material/3_consultarPdmMaterial"
PAGE_SIZE = 500

UPSERT_SQL = """
INSERT INTO material_pdm (
    cod_pdm, cod_classe, cod_grupo, nome_grupo, nome_classe, nome_pdm,
    status_pdm, data_hora_atualizacao
)
VALUES (
    %(cod_pdm)s, %(cod_classe)s, %(cod_grupo)s, %(nome_grupo)s, %(nome_classe)s,
    %(nome_pdm)s, %(status_pdm)s, %(data_hora_atualizacao)s
)
ON CONFLICT (cod_pdm) DO UPDATE SET
cod_classe = EXCLUDED.cod_classe,
cod_grupo = EXCLUDED.cod_grupo,
nome_grupo = EXCLUDED.nome_grupo,
nome_classe = EXCLUDED.nome_classe,
nome_pdm = EXCLUDED.nome_pdm,
status_pdm = EXCLUDED.status_pdm,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
data_hora_carga = now();
"""


def map_material_pdm_row(row: dict[str, Any]) -> MaterialPdmRecord:
    """Map one API resultado object to MaterialPdmRecord.

    Example:
        record = map_material_pdm_row({"codigoPdm": 1, "codigoClasse": 2, ...})
    """
    return MaterialPdmRecord(
        cod_pdm=row["codigoPdm"],
        cod_classe=row["codigoClasse"],
        cod_grupo=row["codigoGrupo"],
        nome_grupo=row["nomeGrupo"],
        nome_classe=row["nomeClasse"],
        nome_pdm=row["nomePdm"],
        status_pdm=row["statusPdm"],
        data_hora_atualizacao=row["dataHoraAtualizacao"],
    )


def main() -> None:
    run_page_batch_ingestion(
        logger_name="material_pdm",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_material_pdm_row,
        table_name="material_pdm",
    )


if __name__ == "__main__":
    main()

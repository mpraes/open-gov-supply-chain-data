from typing import Any

from contracts.material_item import MaterialItemRecord
from etl.ingestion.script_runner import run_script_ingestion

ENDPOINT_PATH = "/modulo-material/4_consultarItemMaterial"
PAGE_SIZE = 500

UPSERT_SQL = """
INSERT INTO material_item (
    cod_item, cod_grupo, nome_grupo, cod_classe, nome_classe, cod_pdm, nome_pdm,
    descricao_item, status_item, item_sustentavel, codigo_ncm, descricao_ncm,
    aplica_margem_preferencia, data_hora_atualizacao
)
VALUES (
    %(cod_item)s, %(cod_grupo)s, %(nome_grupo)s, %(cod_classe)s, %(nome_classe)s,
    %(cod_pdm)s, %(nome_pdm)s, %(descricao_item)s, %(status_item)s,
    %(item_sustentavel)s, %(codigo_ncm)s, %(descricao_ncm)s,
    %(aplica_margem_preferencia)s, %(data_hora_atualizacao)s
)
ON CONFLICT (cod_item) DO UPDATE SET
cod_grupo = EXCLUDED.cod_grupo,
nome_grupo = EXCLUDED.nome_grupo,
cod_classe = EXCLUDED.cod_classe,
nome_classe = EXCLUDED.nome_classe,
cod_pdm = EXCLUDED.cod_pdm,
nome_pdm = EXCLUDED.nome_pdm,
descricao_item = EXCLUDED.descricao_item,
status_item = EXCLUDED.status_item,
item_sustentavel = EXCLUDED.item_sustentavel,
codigo_ncm = EXCLUDED.codigo_ncm,
descricao_ncm = EXCLUDED.descricao_ncm,
aplica_margem_preferencia = EXCLUDED.aplica_margem_preferencia,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
data_hora_carga = now();
"""


def map_material_item_row(row: dict[str, Any]) -> MaterialItemRecord:
    """Map one API resultado object to MaterialItemRecord.

    Example:
        record = map_material_item_row({"codigoItem": 1, "codigoGrupo": 2, ...})
    """
    return MaterialItemRecord(
        cod_item=row["codigoItem"],
        cod_grupo=row["codigoGrupo"],
        nome_grupo=row["nomeGrupo"],
        cod_classe=row["codigoClasse"],
        nome_classe=row["nomeClasse"],
        cod_pdm=row["codigoPdm"],
        nome_pdm=row["nomePdm"],
        descricao_item=row["descricaoItem"],
        status_item=row["statusItem"],
        item_sustentavel=row["itemSustentavel"],
        codigo_ncm=row["codigo_ncm"],
        descricao_ncm=row["descricao_ncm"],
        aplica_margem_preferencia=row["aplica_margem_preferencia"],
        data_hora_atualizacao=row["dataHoraAtualizacao"],
    )


def main() -> None:
    run_script_ingestion(
        logger_name="material_item",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_material_item_row,
        table_name="material_item",
    )


if __name__ == "__main__":
    main()

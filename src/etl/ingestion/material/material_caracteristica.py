from typing import Any

from contracts.material_caracteristica import MaterialCaracteristicaRecord
from etl.ingestion.script_runner import run_script_ingestion

ENDPOINT_PATH = "/modulo-material/7_consultarMaterialCaracteristicas"
PAGE_SIZE = 500

UPSERT_SQL = """
INSERT INTO material_caracteristica (
    cod_item, numero_caracteristica, codigo_caracteristica, codigo_valor_caracteristica,
    nome_caracteristica, status_caracteristica, nome_valor_caracteristica,
    status_valor_caracteristica, item_sustentavel, status_item, sigla_unidade_medida,
    data_hora_atualizacao
)
VALUES (
    %(cod_item)s, %(numero_caracteristica)s, %(codigo_caracteristica)s,
    %(codigo_valor_caracteristica)s, %(nome_caracteristica)s, %(status_caracteristica)s,
    %(nome_valor_caracteristica)s, %(status_valor_caracteristica)s, %(item_sustentavel)s,
    %(status_item)s, %(sigla_unidade_medida)s, %(data_hora_atualizacao)s
)
ON CONFLICT (
    cod_item, numero_caracteristica, codigo_caracteristica, codigo_valor_caracteristica
) DO UPDATE SET
nome_caracteristica = EXCLUDED.nome_caracteristica,
status_caracteristica = EXCLUDED.status_caracteristica,
nome_valor_caracteristica = EXCLUDED.nome_valor_caracteristica,
status_valor_caracteristica = EXCLUDED.status_valor_caracteristica,
item_sustentavel = EXCLUDED.item_sustentavel,
status_item = EXCLUDED.status_item,
sigla_unidade_medida = EXCLUDED.sigla_unidade_medida,
data_hora_atualizacao = EXCLUDED.data_hora_atualizacao,
data_hora_carga = now();
"""


def map_material_caracteristica_row(row: dict[str, Any]) -> MaterialCaracteristicaRecord:
    """Map one API resultado object to MaterialCaracteristicaRecord.

    Example:
        record = map_material_caracteristica_row({"codigoItem": 1, ...})
    """
    return MaterialCaracteristicaRecord(
        cod_item=row["codigoItem"],
        item_sustentavel=row["itemSustentavel"],
        status_item=row["statusItem"],
        codigo_caracteristica=row["codigoCaracteristica"],
        nome_caracteristica=row["nomeCaracteristica"],
        status_caracteristica=row["statusCaracteristica"],
        codigo_valor_caracteristica=row["codigoValorCaracteristica"],
        nome_valor_caracteristica=row["nomeValorCaracteristica"],
        status_valor_caracteristica=row["statusValorCaracteristica"],
        numero_caracteristica=row["numeroCaracteristica"],
        sigla_unidade_medida=row["siglaUnidadeMedida"],
        data_hora_atualizacao=row["dataHoraAtualizacao"],
    )


def main() -> None:
    run_script_ingestion(
        logger_name="material_caracteristica",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_material_caracteristica_row,
        table_name="material_caracteristica",
    )


if __name__ == "__main__":
    main()

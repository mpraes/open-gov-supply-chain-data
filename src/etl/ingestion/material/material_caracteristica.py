"""Ingere características de item de material na tabela material_caracteristica.

O dump sem codigoItem não completa: são 1,7 milhão de linhas e as páginas
profundas estouram o timeout de 30s. Cada item responde numa chamada curta.
"""

from typing import Any

from clients.compras_api import QueryParams
from contracts.material_caracteristica import MaterialCaracteristicaRecord
from etl.ingestion.dest_schema import dest_table
from etl.ingestion.precos.batch_runner import run_preco_batch_ingestion

ENDPOINT_PATH = "/modulo-material/7_consultarMaterialCaracteristicas"
PAGE_SIZE = 500
BATCH_SIZE = 20
PARALLEL_CODES = 4
TABLE_NAME = "material_caracteristica"
CATALOG_TABLE = "material_item"
CATALOG_COLUMN = "cod_item"
# O cursor antigo, material_caracteristica, guarda número de página.
JOB_NAME = "material_caracteristica_item"

UPSERT_SQL = f"""
INSERT INTO {dest_table("material_caracteristica")} (
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
    """Mapeia um objeto resultado da API para MaterialCaracteristicaRecord.

    Exemplo:
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


def caracteristica_item_query_params(code: int) -> QueryParams:
    """Parâmetros de consultarMaterialCaracteristicas para um item CATMAT.

    Exemplo:
        caracteristica_item_query_params(206504) == {"codigoItem": 206504}
    """
    return {"codigoItem": code}


def main() -> None:
    """Grava características dos itens de material_item que ainda não estão no destino."""
    run_preco_batch_ingestion(
        logger_name="material_caracteristica",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_material_caracteristica_row,
        table_name=TABLE_NAME,
        catalog_table=CATALOG_TABLE,
        catalog_column=CATALOG_COLUMN,
        params_for_code=caracteristica_item_query_params,
        absent_dest_table=TABLE_NAME,
        absent_dest_column=CATALOG_COLUMN,
        batch_size=BATCH_SIZE,
        parallel_codes=PARALLEL_CODES,
        job_name=JOB_NAME,
    )


if __name__ == "__main__":
    main()

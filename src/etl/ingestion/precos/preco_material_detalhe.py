from typing import Any

from contracts.preco_material_detalhe import PrecoMaterialDetalheRecord
from etl.ingestion.precos.batch_runner import run_preco_batch_ingestion
from etl.ingestion.precos.map_preco_fields import preco_detalhe_fields
from etl.ingestion.precos.query_params import catalogo_item_query_params

ENDPOINT_PATH = "/modulo-pesquisa-preco/2_consultarMaterialDetalhe"
PAGE_SIZE = 500
BATCH_SIZE = 20
CATALOG_TABLE = "material_item"
CATALOG_COLUMN = "cod_item"

UPSERT_SQL = """
INSERT INTO preco_material_detalhe (
    id_compra, id_item_compra, numero_item_compra, codigo_item_catalogo,
    objeto_compra, descricao_detalhada_item, data_atualizacao_fato
)
VALUES (
    %(id_compra)s, %(id_item_compra)s, %(numero_item_compra)s, %(codigo_item_catalogo)s,
    %(objeto_compra)s, %(descricao_detalhada_item)s, %(data_atualizacao_fato)s
)
ON CONFLICT (id_compra, id_item_compra) DO UPDATE SET
numero_item_compra = EXCLUDED.numero_item_compra,
codigo_item_catalogo = EXCLUDED.codigo_item_catalogo,
objeto_compra = EXCLUDED.objeto_compra,
descricao_detalhada_item = EXCLUDED.descricao_detalhada_item,
data_atualizacao_fato = EXCLUDED.data_atualizacao_fato,
data_hora_carga = now();
"""


def map_preco_material_detalhe_row(row: dict[str, Any]) -> PrecoMaterialDetalheRecord:
    """Map one consultarMaterialDetalhe resultado object.

    Example:
        record = map_preco_material_detalhe_row({"idCompra": "c1", ...})
    """
    return PrecoMaterialDetalheRecord(**preco_detalhe_fields(row))


def main() -> None:
    run_preco_batch_ingestion(
        logger_name="preco_material_detalhe",
        endpoint_path=ENDPOINT_PATH,
        page_size=PAGE_SIZE,
        upsert_sql=UPSERT_SQL,
        map_row=map_preco_material_detalhe_row,
        table_name="preco_material_detalhe",
        catalog_table=CATALOG_TABLE,
        catalog_column=CATALOG_COLUMN,
        params_for_code=catalogo_item_query_params,
        dest_code_column="codigo_item_catalogo",
        dest_date_column="data_atualizacao_fato",
        batch_size=BATCH_SIZE,
    )


if __name__ == "__main__":
    main()

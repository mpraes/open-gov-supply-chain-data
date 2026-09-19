from etl.ingestion.precos.query_params import (
    catalogo_item_query_params,
    material_preco_query_params,
)


def test_material_preco_query_params_uses_item_catalog_tipo() -> None:
    assert material_preco_query_params(123) == {
        "tipo": "codigoItemCatalogo",
        "codigo": "123",
    }


def test_catalogo_item_query_params_uses_codigo_item_catalogo() -> None:
    assert catalogo_item_query_params(7250) == {"codigoItemCatalogo": 7250}

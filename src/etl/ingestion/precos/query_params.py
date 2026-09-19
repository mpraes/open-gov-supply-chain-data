from clients.compras_api import QueryParams


def material_preco_query_params(code: int) -> QueryParams:
    """Query params for consultarMaterial by CATMAT item code.

    Example:
        material_preco_query_params(123) == {"tipo": "codigoItemCatalogo", "codigo": "123"}
    """
    return {"tipo": "codigoItemCatalogo", "codigo": str(code)}


def catalogo_item_query_params(code: int) -> QueryParams:
    """Query params for detalhe and serviço price endpoints.

    Example:
        catalogo_item_query_params(7250) == {"codigoItemCatalogo": 7250}
    """
    return {"codigoItemCatalogo": code}

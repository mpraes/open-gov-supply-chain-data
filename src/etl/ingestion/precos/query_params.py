"""Monta os parâmetros de consulta de consultarMaterial e dos endpoints de detalhe e de serviço."""

from clients.compras_api import QueryParams


def material_preco_query_params(code: int) -> QueryParams:
    """Parâmetros de consulta de consultarMaterial pelo código PDM do CATMAT.

    Exemplo:
        material_preco_query_params(123) == {"tipo": "codigoPdm", "codigo": "123"}
    """
    return {"tipo": "codigoPdm", "codigo": str(code)}


def catalogo_item_query_params(code: int) -> QueryParams:
    """Parâmetros de consulta dos endpoints de detalhe e de preço de serviço.

    Exemplo:
        catalogo_item_query_params(7250) == {"codigoItemCatalogo": 7250}
    """
    return {"codigoItemCatalogo": code}

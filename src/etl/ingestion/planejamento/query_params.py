"""Monta os parâmetros de consulta de consultarPgcDetalhe, consultarPgcDetalheCatalogo e consultarPgcAgregacao."""

from clients.compras_api import QueryParams


def pgc_detalhe_query_params(
    orgao: str,
    ano: int,
    codigo_uasg: str | None = None,
) -> QueryParams:
    """Parâmetros de consulta de consultarPgcDetalhe por órgão e ano do PCA.

    Exemplo:
        pgc_detalhe_query_params("36000", 2026) == {
            "orgao": "36000", "anoPcaProjetoCompra": 2026,
        }
    """
    params: dict[str, str | int] = {
        "orgao": orgao,
        "anoPcaProjetoCompra": ano,
    }
    if codigo_uasg is None:
        return params
    params["codigoUasg"] = codigo_uasg
    return params


def pgc_catalogo_query_params(code: int, *, tipo: str, ano: int) -> QueryParams:
    """Parâmetros de consulta de consultarPgcDetalheCatalogo pelo código de catálogo.

    Exemplo:
        pgc_catalogo_query_params(101, tipo="Material", ano=2026)
    """
    return {"anoPcaProjetoCompra": ano, "tipo": tipo, "codigo": code}


def pgc_agregacao_query_params(orgao: str, ano: int) -> QueryParams:
    """Parâmetros de consulta de consultarPgcAgregacao por órgão e ano.

    Exemplo:
        pgc_agregacao_query_params("36000", 2026) == {"orgao": "36000", "ano": 2026}
    """
    return {"orgao": orgao, "ano": ano}

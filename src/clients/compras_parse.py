"""Interpreta páginas JSON das APIs do compras.gov em linhas de catálogo."""

from clients.compras_types import JsonRow, QueryParams


def page_query_params(
    pagina: int,
    page_size: int | None,
    query_params: QueryParams | None,
) -> dict[str, str | int | bool]:
    """Monta os parâmetros pagina/tamanhoPagina de uma busca de página no compras.gov.

    Exemplo:
        page_query_params(2, 500, {"tipo": "codigoPdm"})["pagina"] == 2
    """
    params: dict[str, str | int | bool] = dict(query_params) if query_params else {}
    params["pagina"] = pagina
    if page_size is not None:
        params["tamanhoPagina"] = page_size
    return params


def parse_resultado_page(payload: object) -> tuple[list[JsonRow], int]:
    """Interpreta uma página `resultado` do compras.gov em linhas e total de páginas.

    Exemplo:
        rows, total = parse_resultado_page({"resultado": [{"id": 1}], "totalPaginas": 1})
    """
    page = _require_json_object(payload, "page payload")
    resultado = page.get("resultado")
    if not isinstance(resultado, list):
        raise ValueError(
            f"expected data['resultado'] to be a list, got {type(resultado).__name__}: {resultado!r}"
        )
    total_paginas = page.get("totalPaginas", 1)
    if not isinstance(total_paginas, int) or total_paginas < 0:
        raise ValueError(
            f"expected data['totalPaginas'] to be int >= 0, got {total_paginas!r}"
        )
    return [
        _require_row_dict(row, index) for index, row in enumerate(resultado)
    ], total_paginas


def parse_releases_page(payload: object, pagina: int) -> tuple[list[JsonRow], int]:
    """Interpreta uma página de `releases` OCDS em linhas e num sentinela de próxima página.

    Exemplo:
        rows, total = parse_releases_page({"releases": [], "links": {}}, pagina=1)
    """
    page = _require_json_object(payload, "OCDS payload")
    releases = page.get("releases")
    if not isinstance(releases, list):
        raise ValueError(
            f"expected data['releases'] to be a list, got {type(releases).__name__}: {releases!r}"
        )
    rows = [_require_row_dict(row, index) for index, row in enumerate(releases)]
    return rows, _ocds_total_pages(page, pagina, rows)


def parse_json_array(payload: object) -> list[JsonRow]:
    """Interpreta um endpoint de array JSON em objetos de linha.

    Exemplo:
        parse_json_array([{"id": 1}]) == [{"id": 1}]
    """
    if not isinstance(payload, list):
        raise ValueError(
            f"expected JSON array payload, got {type(payload).__name__}: {payload!r}"
        )
    return [_require_row_dict(row, index) for index, row in enumerate(payload)]


def _require_json_object(payload: object, label: str) -> dict[str, object]:
    """Exige um objeto JSON e devolve o dicionário."""
    if not isinstance(payload, dict):
        raise ValueError(
            f"expected JSON object {label}, got {type(payload).__name__}: {payload!r}"
        )
    return payload


def _ocds_total_pages(
    payload: dict[str, object], pagina: int, rows: list[JsonRow]
) -> int:
    """Devolve 0 na primeira página vazia, pagina + 1 quando há links.next e pagina no fim."""
    if not rows and pagina == 1:
        return 0
    links = payload.get("links")
    if isinstance(links, dict) and links.get("next"):
        return pagina + 1
    return pagina


def _require_row_dict(row: object, index: int) -> JsonRow:
    """Exige que a linha seja um objeto e devolve o dicionário."""
    if not isinstance(row, dict):
        raise ValueError(
            f"expected resultado[{index}] to be an object, got {type(row).__name__}: {row!r}"
        )
    return row

from collections.abc import Callable
from typing import Any

import requests

HttpGet = Callable[..., Any]


def fetch_all_resultado_pages(
    url: str,
    headers: dict[str, str],
    *,
    page_size: int | None = 500,
    timeout: int = 30,
    http_get: HttpGet = requests.get,
) -> list[dict[str, Any]]:
    """Fetch every page of a compras.gov paginated `resultado` endpoint.

    Example:
        rows = fetch_all_resultado_pages(url, headers, page_size=500)
    """
    rows: list[dict[str, Any]] = []
    pagina = 1
    total_paginas = 1
    while pagina <= total_paginas:
        page_rows, total_paginas = _fetch_one_resultado_page(
            url, headers, pagina=pagina, page_size=page_size, timeout=timeout, http_get=http_get
        )
        rows.extend(page_rows)
        pagina += 1
    return rows


def _fetch_one_resultado_page(
    url: str,
    headers: dict[str, str],
    *,
    pagina: int,
    page_size: int | None,
    timeout: int,
    http_get: HttpGet,
) -> tuple[list[dict[str, Any]], int]:
    params: dict[str, int] = {"pagina": pagina}
    if page_size is not None:
        params["tamanhoPagina"] = page_size
    response = http_get(url, headers=headers, params=params, timeout=timeout)
    response.raise_for_status()
    payload = response.json()
    return _parse_resultado_page(payload)


def _parse_resultado_page(payload: object) -> tuple[list[dict[str, Any]], int]:
    if not isinstance(payload, dict):
        raise ValueError(
            f"expected JSON object page payload, got {type(payload).__name__}: {payload!r}"
        )
    resultado = payload.get("resultado")
    if not isinstance(resultado, list):
        raise ValueError(
            f"expected data['resultado'] to be a list, got {type(resultado).__name__}: {resultado!r}"
        )
    total_paginas = payload.get("totalPaginas", 1)
    if not isinstance(total_paginas, int) or total_paginas < 1:
        raise ValueError(
            f"expected data['totalPaginas'] to be int >= 1, got {total_paginas!r}"
        )
    typed_rows = [_require_row_dict(row, index) for index, row in enumerate(resultado)]
    return typed_rows, total_paginas


def _require_row_dict(row: object, index: int) -> dict[str, Any]:
    if not isinstance(row, dict):
        raise ValueError(
            f"expected resultado[{index}] to be an object, got {type(row).__name__}: {row!r}"
        )
    return row

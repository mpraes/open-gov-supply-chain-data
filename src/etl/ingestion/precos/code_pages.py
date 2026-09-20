from collections.abc import Callable
from typing import Any

from clients.compras_api import CodeParamsFn, fetch_resultado_pages_for_codes
from etl.ingestion.pipeline import FetchPages
from etl.ingestion.precos.catalog_codes import list_int_column

FetchForCodes = Callable[..., list[dict[str, Any]]]


def build_codigo_fetch_pages(
    conn: Any,
    catalog_sql: str,
    params_for_code: CodeParamsFn,
    *,
    fetch_for_codes: FetchForCodes = fetch_resultado_pages_for_codes,
    pause_seconds: float = 0,
) -> FetchPages:
    """Build a pipeline fetch_pages that queries one catalog code column.

    Example:
        fetch_pages = build_codigo_fetch_pages(
            conn, "SELECT cod_item FROM material_item",
            lambda code: {"codigo": str(code)},
        )
    """
    codes = list_int_column(conn, catalog_sql)
    return _bind_codigo_fetch_pages(
        codes, params_for_code, fetch_for_codes, pause_seconds
    )


def _bind_codigo_fetch_pages(
    codes: list[int],
    params_for_code: CodeParamsFn,
    fetch_for_codes: FetchForCodes,
    pause_seconds: float,
) -> FetchPages:
    def fetch_pages(
        url: str,
        headers: dict[str, str],
        *,
        page_size: int | None = 500,
    ) -> list[dict[str, Any]]:
        return fetch_for_codes(
            url,
            headers,
            codes=codes,
            params_for_code=params_for_code,
            page_size=page_size,
            pause_seconds=pause_seconds,
        )

    return fetch_pages

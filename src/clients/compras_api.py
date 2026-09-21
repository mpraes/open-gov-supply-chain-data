from concurrent.futures import Future, ThreadPoolExecutor
from logging import Logger
from time import sleep as time_sleep

import requests

from clients.compras_http import DEFAULT_MAX_RETRIES, get_ok_response
from clients.compras_parse import (
    page_query_params,
    parse_json_array,
    parse_releases_page,
    parse_resultado_page,
)
from clients.compras_types import (
    CodePagesFetch,
    CodeParamsFn,
    HttpGet,
    JsonRow,
    QueryParams,
    SleepFn,
)

__all__ = [
    "CodeParamsFn",
    "DEFAULT_MAX_RETRIES",
    "HttpGet",
    "QueryParams",
    "SleepFn",
    "fetch_all_resultado_pages",
    "fetch_one_json_array_page",
    "fetch_one_releases_page",
    "fetch_one_resultado_page",
    "fetch_resultado_pages_for_codes",
]


def fetch_all_resultado_pages(
    url: str,
    headers: dict[str, str],
    *,
    page_size: int | None = 500,
    timeout: int = 30,
    http_get: HttpGet = requests.get,
    query_params: QueryParams | None = None,
    sleep_fn: SleepFn = time_sleep,
    max_retries: int = DEFAULT_MAX_RETRIES,
) -> list[JsonRow]:
    """Fetch every page of a compras.gov paginated `resultado` endpoint.

    Example:
        rows = fetch_all_resultado_pages(
            url, headers, page_size=500,
            query_params={"tipo": "codigoItemCatalogo", "codigo": "123"},
        )
    """
    rows: list[JsonRow] = []
    pagina = 1
    total_paginas = 1
    while pagina <= total_paginas:
        page_rows, total_paginas = _fetch_one_resultado_page(
            url,
            headers,
            pagina=pagina,
            page_size=page_size,
            timeout=timeout,
            http_get=http_get,
            query_params=query_params,
            sleep_fn=sleep_fn,
            max_retries=max_retries,
        )
        rows.extend(page_rows)
        pagina += 1
    return rows


def fetch_one_resultado_page(
    url: str,
    headers: dict[str, str],
    *,
    pagina: int,
    page_size: int | None = 500,
    timeout: int = 30,
    http_get: HttpGet = requests.get,
    query_params: QueryParams | None = None,
    sleep_fn: SleepFn = time_sleep,
    max_retries: int = DEFAULT_MAX_RETRIES,
    log: Logger | None = None,
) -> tuple[list[JsonRow], int]:
    """Fetch one compras.gov `resultado` page and its total page count.

    Example:
        rows, total = fetch_one_resultado_page(url, headers, pagina=2, page_size=500)
    """
    return _fetch_one_resultado_page(
        url,
        headers,
        pagina=pagina,
        page_size=page_size,
        timeout=timeout,
        http_get=http_get,
        query_params=query_params,
        sleep_fn=sleep_fn,
        max_retries=max_retries,
        log=log,
    )


def fetch_one_releases_page(
    url: str,
    headers: dict[str, str],
    *,
    pagina: int,
    page_size: int | None = 500,
    timeout: int = 30,
    http_get: HttpGet = requests.get,
    query_params: QueryParams | None = None,
    sleep_fn: SleepFn = time_sleep,
    max_retries: int = DEFAULT_MAX_RETRIES,
    log: Logger | None = None,
) -> tuple[list[JsonRow], int]:
    """Fetch one OCDS `releases` page using page/offSet.

    Example:
        rows, total = fetch_one_releases_page(url, headers, pagina=1, page_size=10)
    """
    params = dict(query_params) if query_params else {}
    params["page"] = pagina
    if page_size is not None:
        params["offSet"] = page_size
    response = get_ok_response(
        url, headers, params, timeout, http_get, sleep_fn, max_retries, log
    )
    return parse_releases_page(response.json(), pagina)


def fetch_one_json_array_page(
    url: str,
    headers: dict[str, str],
    *,
    pagina: int,
    page_size: int | None = 500,
    timeout: int = 30,
    http_get: HttpGet = requests.get,
    query_params: QueryParams | None = None,
    sleep_fn: SleepFn = time_sleep,
    max_retries: int = DEFAULT_MAX_RETRIES,
    log: Logger | None = None,
) -> tuple[list[JsonRow], int]:
    """Fetch a non-paginated JSON array endpoint as a single page.

    Example:
        rows, total = fetch_one_json_array_page(url, headers, pagina=1)
    """
    if pagina > 1:
        return [], 1
    params = dict(query_params) if query_params else {}
    response = get_ok_response(
        url, headers, params, timeout, http_get, sleep_fn, max_retries, log
    )
    return parse_json_array(response.json()), 1


def fetch_resultado_pages_for_codes(
    url: str,
    headers: dict[str, str],
    *,
    codes: list[int],
    params_for_code: CodeParamsFn,
    page_size: int | None = 500,
    timeout: int = 30,
    http_get: HttpGet = requests.get,
    pause_seconds: float = 0,
    sleep_fn: SleepFn = time_sleep,
    max_retries: int = DEFAULT_MAX_RETRIES,
    parallel_codes: int = 1,
) -> list[JsonRow]:
    """Fetch paginated `resultado` rows for each catalog code.

    Example:
        rows = fetch_resultado_pages_for_codes(
            url, headers, codes=[10, 20],
            params_for_code=lambda code: {"codigo": str(code)},
            parallel_codes=4,
        )
    """
    _require_parallel_codes(parallel_codes)
    resolved = _params_for_each_code(codes, params_for_code)
    fetch_one = _bind_code_pages_fetch(
        url, headers, page_size, timeout, http_get, sleep_fn, max_retries
    )
    if parallel_codes == 1:
        return _fetch_code_pages_serial(resolved, fetch_one, pause_seconds, sleep_fn)
    return _fetch_code_pages_parallel(resolved, fetch_one, parallel_codes)


def _require_parallel_codes(parallel_codes: int) -> None:
    if parallel_codes < 1:
        raise ValueError(f"parallel_codes expected int >= 1, got {parallel_codes!r}")


def _params_for_each_code(
    codes: list[int], params_for_code: CodeParamsFn
) -> list[QueryParams]:
    return [dict(params_for_code(code)) for code in codes]


def _bind_code_pages_fetch(
    url: str,
    headers: dict[str, str],
    page_size: int | None,
    timeout: int,
    http_get: HttpGet,
    sleep_fn: SleepFn,
    max_retries: int,
) -> CodePagesFetch:
    def fetch_one(query_params: QueryParams) -> list[JsonRow]:
        return fetch_all_resultado_pages(
            url,
            headers,
            page_size=page_size,
            timeout=timeout,
            http_get=http_get,
            query_params=query_params,
            sleep_fn=sleep_fn,
            max_retries=max_retries,
        )

    return fetch_one


def _fetch_code_pages_serial(
    resolved: list[QueryParams],
    fetch_one: CodePagesFetch,
    pause_seconds: float,
    sleep_fn: SleepFn,
) -> list[JsonRow]:
    rows: list[JsonRow] = []
    for index, query_params in enumerate(resolved):
        _pause_before_code(index, pause_seconds, sleep_fn)
        rows.extend(fetch_one(query_params))
    return rows


def _fetch_code_pages_parallel(
    resolved: list[QueryParams],
    fetch_one: CodePagesFetch,
    parallel_codes: int,
) -> list[JsonRow]:
    with ThreadPoolExecutor(max_workers=parallel_codes) as pool:
        futures = [pool.submit(fetch_one, params) for params in resolved]
        return _rows_from_code_futures(futures)


def _rows_from_code_futures(
    futures: list[Future[list[JsonRow]]],
) -> list[JsonRow]:
    try:
        batches = [future.result() for future in futures]
    except BaseException:
        for future in futures:
            future.cancel()
        raise
    return _concat_row_batches(batches)


def _concat_row_batches(batches: list[list[JsonRow]]) -> list[JsonRow]:
    rows: list[JsonRow] = []
    for batch in batches:
        rows.extend(batch)
    return rows


def _fetch_one_resultado_page(
    url: str,
    headers: dict[str, str],
    *,
    pagina: int,
    page_size: int | None,
    timeout: int,
    http_get: HttpGet,
    query_params: QueryParams | None,
    sleep_fn: SleepFn,
    max_retries: int,
    log: Logger | None = None,
) -> tuple[list[JsonRow], int]:
    params = page_query_params(pagina, page_size, query_params)
    response = get_ok_response(
        url, headers, params, timeout, http_get, sleep_fn, max_retries, log
    )
    return parse_resultado_page(response.json())


def _pause_before_code(index: int, pause_seconds: float, sleep_fn: SleepFn) -> None:
    if index == 0 or pause_seconds <= 0:
        return
    sleep_fn(pause_seconds)

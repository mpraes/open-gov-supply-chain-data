from collections.abc import Callable, Mapping
from typing import Any
from time import sleep as time_sleep

from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import Timeout as RequestsTimeout

import requests

HttpGet = Callable[..., Any]
SleepFn = Callable[[float], None]
QueryParams = Mapping[str, str | int | bool]
CodeParamsFn = Callable[[int], QueryParams]

DEFAULT_MAX_RETRIES = 5


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
) -> list[dict[str, Any]]:
    """Fetch every page of a compras.gov paginated `resultado` endpoint.

    Example:
        rows = fetch_all_resultado_pages(
            url, headers, page_size=500,
            query_params={"tipo": "codigoItemCatalogo", "codigo": "123"},
        )
    """
    rows: list[dict[str, Any]] = []
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
) -> tuple[list[dict[str, Any]], int]:
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
    )


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
) -> list[dict[str, Any]]:
    """Fetch paginated `resultado` rows for each catalog code.

    Example:
        rows = fetch_resultado_pages_for_codes(
            url, headers, codes=[10, 20],
            params_for_code=lambda code: {"codigo": str(code)},
        )
    """
    rows: list[dict[str, Any]] = []
    for index, code in enumerate(codes):
        _pause_before_code(index, pause_seconds, sleep_fn)
        rows.extend(
            fetch_all_resultado_pages(
                url,
                headers,
                page_size=page_size,
                timeout=timeout,
                http_get=http_get,
                query_params=params_for_code(code),
                sleep_fn=sleep_fn,
                max_retries=max_retries,
            )
        )
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
) -> tuple[list[dict[str, Any]], int]:
    params = _page_query_params(pagina, page_size, query_params)
    response = _get_ok_response(
        url, headers, params, timeout, http_get, sleep_fn, max_retries
    )
    return _parse_resultado_page(response.json())


def _pause_before_code(index: int, pause_seconds: float, sleep_fn: SleepFn) -> None:
    if index == 0 or pause_seconds <= 0:
        return
    sleep_fn(pause_seconds)


def _get_ok_response(
    url: str,
    headers: dict[str, str],
    params: dict[str, str | int | bool],
    timeout: int,
    http_get: HttpGet,
    sleep_fn: SleepFn,
    max_retries: int,
) -> Any:
    last_response: Any = None
    for attempt in range(max_retries + 1):
        try:
            last_response = http_get(url, headers=headers, params=params, timeout=timeout)
        except (RequestsConnectionError, RequestsTimeout):
            if attempt < max_retries:
                sleep_fn(float(min(2**attempt, 16)))
                continue
            raise
        if getattr(last_response, "status_code", 200) != 429:
            last_response.raise_for_status()
            return last_response
        if attempt < max_retries:
            sleep_fn(_retry_wait_seconds(last_response, attempt))
            continue
        last_response.raise_for_status()
    raise RuntimeError(f"429 retry loop exhausted after {max_retries} retries")


def _retry_wait_seconds(response: Any, attempt: int) -> float:
    retry_after = _retry_after_header_seconds(response)
    if retry_after is not None:
        return retry_after
    return float(min(2**attempt, 16))


def _retry_after_header_seconds(response: Any) -> float | None:
    headers = getattr(response, "headers", None)
    if not isinstance(headers, Mapping):
        return None
    raw = headers.get("Retry-After", headers.get("retry-after"))
    if raw is None:
        return None
    return _parse_retry_after_seconds(raw)


def _parse_retry_after_seconds(raw: object) -> float:
    if isinstance(raw, bool) or not isinstance(raw, (int, float, str)):
        raise ValueError(
            f"Retry-After expected a number of seconds, got {type(raw).__name__}: {raw!r}"
        )
    seconds = float(raw)
    if seconds < 0:
        raise ValueError(f"Retry-After must be >= 0, got {raw!r}")
    return seconds


def _page_query_params(
    pagina: int,
    page_size: int | None,
    query_params: QueryParams | None,
) -> dict[str, str | int | bool]:
    params: dict[str, str | int | bool] = dict(query_params) if query_params else {}
    params["pagina"] = pagina
    if page_size is not None:
        params["tamanhoPagina"] = page_size
    return params


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
    if not isinstance(total_paginas, int) or total_paginas < 0:
        raise ValueError(
            f"expected data['totalPaginas'] to be int >= 0, got {total_paginas!r}"
        )
    typed_rows = [_require_row_dict(row, index) for index, row in enumerate(resultado)]
    return typed_rows, total_paginas


def _require_row_dict(row: object, index: int) -> dict[str, Any]:
    if not isinstance(row, dict):
        raise ValueError(
            f"expected resultado[{index}] to be an object, got {type(row).__name__}: {row!r}"
        )
    return row

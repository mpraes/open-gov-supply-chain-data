from collections.abc import Mapping
from logging import Logger

from requests.exceptions import ConnectionError as RequestsConnectionError
from requests.exceptions import Timeout as RequestsTimeout

from clients.compras_types import HttpGet, HttpResponse, SleepFn
from observability.logging_json import log_warning

DEFAULT_MAX_RETRIES = 5
RETRYABLE_HTTP_STATUSES = frozenset({400, 429, 500, 502, 503})
_HTTP_ERROR_BODY_LIMIT = 500


def get_ok_response(
    url: str,
    headers: dict[str, str],
    params: dict[str, str | int | bool],
    timeout: int,
    http_get: HttpGet,
    sleep_fn: SleepFn,
    max_retries: int,
    log: Logger | None = None,
) -> HttpResponse:
    """GET a URL, retrying transient HTTP and transport errors.

    Example:
        response = get_ok_response(url, headers, params, 30, http_get, sleep, 5)
    """
    last_response: HttpResponse | None = None
    for attempt in range(max_retries + 1):
        last_response = _request_or_retry_transport(
            url, headers, params, timeout, http_get, sleep_fn, max_retries, log, attempt
        )
        if last_response is None:
            continue
        if _retry_http_status(last_response, attempt, max_retries, sleep_fn, log):
            continue
        _raise_if_bad_status(last_response)
        return last_response
    raise RuntimeError(f"HTTP retry loop exhausted after {max_retries} retries")


def _request_or_retry_transport(
    url: str,
    headers: dict[str, str],
    params: dict[str, str | int | bool],
    timeout: int,
    http_get: HttpGet,
    sleep_fn: SleepFn,
    max_retries: int,
    log: Logger | None,
    attempt: int,
) -> HttpResponse | None:
    try:
        return http_get(url, headers=headers, params=params, timeout=timeout)
    except (RequestsConnectionError, RequestsTimeout) as exc:
        _retry_transport_error(exc, attempt, max_retries, sleep_fn, log)
        return None


def _retry_http_status(
    response: HttpResponse,
    attempt: int,
    max_retries: int,
    sleep_fn: SleepFn,
    log: Logger | None,
) -> bool:
    status = getattr(response, "status_code", 200)
    if status not in RETRYABLE_HTTP_STATUSES or attempt >= max_retries:
        return False
    wait_s = _retry_wait_seconds(response, attempt)
    _log_api_retry(log, attempt, wait_s, status=status)
    sleep_fn(wait_s)
    return True


def _raise_if_bad_status(response: HttpResponse) -> None:
    try:
        response.raise_for_status()
    except Exception as exc:
        body = http_error_body(response)
        if body == "":
            raise
        raise RuntimeError(f"{exc} body={body!r}") from exc


def http_error_body(response: HttpResponse) -> str:
    """Return a short response body snippet for HTTP error messages.

    Example:
        http_error_body(response) == "Token malformado"
    """
    raw = getattr(response, "text", "")
    if not isinstance(raw, str):
        return ""
    return raw[:_HTTP_ERROR_BODY_LIMIT]


def _log_api_retry(
    log: Logger | None,
    attempt: int,
    wait_s: float,
    **fields: object,
) -> None:
    if log is None:
        return
    log_warning(log, "api_retry", attempt=attempt + 1, wait_s=wait_s, **fields)


def _retry_transport_error(
    exc: BaseException,
    attempt: int,
    max_retries: int,
    sleep_fn: SleepFn,
    log: Logger | None,
) -> None:
    if attempt >= max_retries:
        raise exc
    wait_s = float(min(2**attempt, 16))
    _log_api_retry(log, attempt, wait_s, error=type(exc).__name__)
    sleep_fn(wait_s)


def _retry_wait_seconds(response: HttpResponse, attempt: int) -> float:
    retry_after = _retry_after_header_seconds(response)
    if retry_after is not None:
        return retry_after
    return float(min(2**attempt, 16))


def _retry_after_header_seconds(response: HttpResponse) -> float | None:
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

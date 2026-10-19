"""Tipos e protocolos do cliente HTTP do compras.gov."""

from collections.abc import Callable, Mapping
from typing import Any, Protocol

QueryParams = Mapping[str, str | int | bool]
SleepFn = Callable[[float], None]
CodeParamsFn = Callable[[int], QueryParams]
JsonRow = dict[str, Any]


class HttpResponse(Protocol):
    """Resposta HTTP mínima consumida pelo cliente do compras.gov."""

    status_code: int
    text: str
    headers: Mapping[str, str]

    def raise_for_status(self) -> None:
        """Levanta erro quando o status HTTP indica falha."""
        ...

    def json(self) -> object:
        """Decodifica o corpo da resposta como JSON."""
        ...


HttpGet = Callable[..., HttpResponse]
CodePagesFetch = Callable[[QueryParams], list[JsonRow]]

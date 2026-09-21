from collections.abc import Callable, Mapping
from typing import Any, Protocol

QueryParams = Mapping[str, str | int | bool]
SleepFn = Callable[[float], None]
CodeParamsFn = Callable[[int], QueryParams]
JsonRow = dict[str, Any]


class HttpResponse(Protocol):
    status_code: int
    text: str
    headers: Mapping[str, str]

    def raise_for_status(self) -> None: ...

    def json(self) -> object: ...


HttpGet = Callable[..., HttpResponse]
CodePagesFetch = Callable[[QueryParams], list[JsonRow]]

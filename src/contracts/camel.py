import re
from typing import Any

_CAMEL_BOUNDARY = re.compile(r"(?<=[a-z0-9])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])")


def camel_to_snake(name: str) -> str:
    """Convert an API camelCase or PascalCase key to snake_case.

    Example:
        camel_to_snake("idCompra") == "id_compra"
    """
    return _CAMEL_BOUNDARY.sub("_", name).lower()


def snake_row(row: dict[str, Any]) -> dict[str, Any]:
    """Rename all keys of one API object to snake_case.

    Example:
        snake_row({"idCompra": "1"}) == {"id_compra": "1"}
    """
    return {camel_to_snake(key): value for key, value in row.items()}

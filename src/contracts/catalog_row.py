from typing import Any, ClassVar

from pydantic import BaseModel, ConfigDict, model_validator

from contracts.coerce import coerce_optional_decimal
from contracts.text_normalize import upper_optional


def normalize_catalog_row(
    data: dict[str, Any],
    *,
    float_fields: frozenset[str],
    name_fields: frozenset[str],
) -> dict[str, Any]:
    """Uppercase name fields and coerce optional decimal amounts.

    Example:
        normalize_catalog_row({"objeto": " x "}, float_fields=frozenset(), name_fields=frozenset({"objeto"}))
    """
    out: dict[str, Any] = {}
    for key, value in data.items():
        if key in float_fields:
            out[key] = coerce_optional_decimal(value)
            continue
        if key in name_fields and isinstance(value, str):
            out[key] = upper_optional(value)
            continue
        out[key] = value
    return out


class CatalogRow(BaseModel):
    """Base row that keeps extra API columns after snake_case mapping.

    Example:
        class Item(CatalogRow):
            id_compra: str
    """

    model_config = ConfigDict(strict=True, extra="allow")

    _float_fields: ClassVar[frozenset[str]] = frozenset()
    _name_fields: ClassVar[frozenset[str]] = frozenset()

    @model_validator(mode="before")
    @classmethod
    def normalize_known_fields(cls, data: object) -> object:
        if not isinstance(data, dict):
            return data
        return normalize_catalog_row(
            data,
            float_fields=cls._float_fields,
            name_fields=cls._name_fields,
        )

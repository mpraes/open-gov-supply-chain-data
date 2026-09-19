"""Coercion helpers for API values that mix ints, strings, and numbers."""


def coerce_id_text(value: object, field_label: str) -> str:
    """Turn an int or str identifier into a stripped string.

    Example:
        coerce_id_text(12, "id_compra") == "12"
    """
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise ValueError(
            f"{field_label} expected int or str, got {type(value).__name__}: {value!r}"
        )
    text = str(value).strip()
    if not text:
        raise ValueError(f"{field_label} must be non-empty, got {value!r}")
    return text


def coerce_optional_float(value: object) -> float | None:
    """Coerce optional numeric API fields; bools are rejected.

    Example:
        coerce_optional_float(3) == 3.0
    """
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(
            f"expected int or float, got {type(value).__name__}: {value!r}"
        )
    return float(value)

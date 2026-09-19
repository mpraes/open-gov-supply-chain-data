"""Shared text normalization for catalog Pydantic contracts."""


def upper_non_empty(value: str, field_label: str) -> str:
    """Strip and uppercase a required text field.

    Example:
        upper_non_empty("  abc ", "nome") == "ABC"
    """
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_label} must be non-empty")
    return cleaned.upper()


def upper_optional(value: str | None) -> str | None:
    """Strip and uppercase an optional text field; blank becomes None.

    Example:
        upper_optional("  x ") == "X"
    """
    cleaned = strip_optional(value)
    if cleaned is None:
        return None
    return cleaned.upper()


def strip_optional(value: str | None) -> str | None:
    """Strip an optional text field; blank becomes None.

    Example:
        strip_optional("  12 ") == "12"
    """
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    return cleaned

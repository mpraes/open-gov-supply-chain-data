"""Normalização de texto compartilhada pelos contratos Pydantic de catálogo."""


def upper_non_empty(value: str, field_label: str) -> str:
    """Remove espaços e converte um campo de texto obrigatório para maiúsculas.

    Exemplo:
        upper_non_empty("  abc ", "nome") == "ABC"
    """
    cleaned = value.strip()
    if not cleaned:
        raise ValueError(f"{field_label} must be non-empty")
    return cleaned.upper()


def upper_optional(value: str | None) -> str | None:
    """Remove espaços e converte um campo de texto opcional para maiúsculas; vazio vira None.

    Exemplo:
        upper_optional("  x ") == "X"
    """
    cleaned = strip_optional(value)
    if cleaned is None:
        return None
    return cleaned.upper()


def strip_optional(value: str | None) -> str | None:
    """Remove espaços de um campo de texto opcional; vazio vira None.

    Exemplo:
        strip_optional("  12 ") == "12"
    """
    if value is None:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    return cleaned

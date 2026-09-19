import pytest
from pydantic import ValidationError

from contracts.text_normalize import strip_optional, upper_non_empty, upper_optional


def test_upper_non_empty_strips_and_uppercases() -> None:
    assert upper_non_empty("  ab ", "nome") == "AB"


def test_upper_non_empty_rejects_blank() -> None:
    with pytest.raises(ValueError, match="nome must be non-empty"):
        upper_non_empty("  ", "nome")


def test_upper_optional_blank_becomes_none() -> None:
    assert upper_optional("  ") is None
    assert upper_optional(None) is None
    assert upper_optional(" x ") == "X"


def test_strip_optional_keeps_case() -> None:
    assert strip_optional("  12 ") == "12"
    assert strip_optional("  ") is None
    assert strip_optional(None) is None

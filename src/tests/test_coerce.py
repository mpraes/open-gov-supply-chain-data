import pytest

from contracts.coerce import (
    coerce_id_text,
    coerce_optional_decimal,
    coerce_optional_float,
    coerce_optional_id_text,
)


def test_coerce_id_text_accepts_int_and_str() -> None:
    assert coerce_id_text(12, "id_compra") == "12"
    assert coerce_id_text("  ab-1 ", "id_compra") == "ab-1"


def test_coerce_id_text_rejects_blank_and_bool() -> None:
    with pytest.raises(ValueError, match="id_compra must be non-empty"):
        coerce_id_text("  ", "id_compra")
    with pytest.raises(ValueError, match="id_compra expected int or str, got bool: True"):
        coerce_id_text(True, "id_compra")


def test_coerce_optional_float_accepts_int_and_float() -> None:
    assert coerce_optional_float(None) is None
    assert coerce_optional_float(3) == 3.0
    assert coerce_optional_float(1.5) == 1.5


def test_coerce_optional_float_rejects_bool_and_str() -> None:
    with pytest.raises(ValueError, match="expected int or float, got bool: True"):
        coerce_optional_float(True)
    with pytest.raises(ValueError, match="expected int or float, got str: '1'"):
        coerce_optional_float("1")


def test_coerce_optional_decimal_accepts_numeric_string() -> None:
    assert coerce_optional_decimal(" 10.5 ") == 10.5
    assert coerce_optional_decimal("1,25") == 1.25
    assert coerce_optional_decimal("") is None
    assert coerce_optional_decimal(3) == 3.0


def test_coerce_optional_id_text_allows_blank_as_none() -> None:
    assert coerce_optional_id_text(None, "nome") is None
    assert coerce_optional_id_text("  ", "nome") is None
    assert coerce_optional_id_text(12, "nome") == "12"

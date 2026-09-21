import pytest

from clients.compras_parse import parse_json_array, parse_resultado_page


def test_parse_resultado_page_rejects_non_object_payload() -> None:
    with pytest.raises(ValueError, match="expected JSON object page payload, got list"):
        parse_resultado_page([])


def test_parse_json_array_rejects_non_list_payload() -> None:
    with pytest.raises(ValueError, match="expected JSON array payload, got dict"):
        parse_json_array({"resultado": []})

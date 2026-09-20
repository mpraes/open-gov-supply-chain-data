import pytest

from etl.ingestion.dest_schema import DEST_SCHEMA, dest_table, search_path_options


def test_dest_table_qualifies_with_staging() -> None:
    assert DEST_SCHEMA == "staging"
    assert dest_table("preco_material") == "staging.preco_material"


def test_dest_table_rejects_unsafe_identifier() -> None:
    with pytest.raises(ValueError, match="table expected snake_case identifier"):
        dest_table("preco;drop")


def test_search_path_options_targets_staging() -> None:
    assert search_path_options() == "-c search_path=staging"

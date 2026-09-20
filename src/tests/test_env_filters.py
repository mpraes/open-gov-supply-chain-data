from pathlib import Path

import pytest

from etl.ingestion.env_filters import (
    optional_text,
    require_int_value,
    require_iso_date_pair,
    require_text,
)


def test_require_iso_date_pair_reads_keys() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"A": "2024-01-01", "B": "2024-12-31"}[name]

    assert require_iso_date_pair(Path(".env"), load_secret, "A", "B") == (
        "2024-01-01",
        "2024-12-31",
    )


def test_require_int_value_rejects_letters() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return "x"

    with pytest.raises(ValueError, match="MOD expected digits"):
        require_int_value(Path(".env"), load_secret, "MOD")


def test_require_text_strips() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return "  36000  "

    assert require_text(Path(".env"), load_secret, "ORGAO") == "36000"


def test_optional_text_missing_is_none() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        raise KeyError(name)

    assert optional_text(Path(".env"), load_secret, "X") is None

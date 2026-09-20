from pathlib import Path

import pytest

from etl.ingestion.legado.filters import (
    legado_ano,
    legado_date_range,
    legado_modalidade,
    legado_optional_uasg,
)


def test_legado_date_range_reads_iso_dates() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {
            "LEGADO_DATA_INICIAL": "2024-01-01",
            "LEGADO_DATA_FINAL": "2024-12-31",
        }[name]

    assert legado_date_range(Path(".env"), load_secret) == ("2024-01-01", "2024-12-31")


def test_legado_date_range_rejects_invalid_date() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {
            "LEGADO_DATA_INICIAL": "01/01/2024",
            "LEGADO_DATA_FINAL": "2024-12-31",
        }[name]

    with pytest.raises(ValueError, match="LEGADO_DATA_INICIAL expected YYYY-MM-DD"):
        legado_date_range(Path(".env"), load_secret)


def test_legado_ano_reads_year() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"LEGADO_ANO": "2024"}[name]

    assert legado_ano(Path(".env"), load_secret) == 2024


def test_legado_ano_rejects_year_outside_range() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"LEGADO_ANO": "1999"}[name]

    with pytest.raises(ValueError, match="LEGADO_ANO expected year 2000-2100, got 1999"):
        legado_ano(Path(".env"), load_secret)


def test_legado_modalidade_reads_int() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"LEGADO_MODALIDADE": "5"}[name]

    assert legado_modalidade(Path(".env"), load_secret) == 5


def test_legado_optional_uasg_returns_none_when_missing() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        raise KeyError(name)

    assert legado_optional_uasg(Path(".env"), load_secret) is None


def test_legado_optional_uasg_parses_int() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"LEGADO_UASG": "153001"}[name]

    assert legado_optional_uasg(Path(".env"), load_secret) == 153001

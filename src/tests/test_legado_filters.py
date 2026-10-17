from pathlib import Path

import pytest

from etl.ingestion.legado.filters import (
    LEGADO_ITEM_MODALIDADES,
    legado_ano,
    legado_date_range,
    legado_modalidades,
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


def test_legado_modalidades_reads_one_code() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"LEGADO_MODALIDADE": "5"}[name]

    assert legado_modalidades(Path(".env"), load_secret) == (5,)


def test_legado_modalidades_defaults_to_all_siasg_codes_when_missing() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        raise KeyError(name)

    assert legado_modalidades(Path(".env"), load_secret) == LEGADO_ITEM_MODALIDADES
    assert LEGADO_ITEM_MODALIDADES == (1, 2, 3, 4, 5, 6, 7, 20)


def test_legado_modalidades_rejects_non_digits() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"LEGADO_MODALIDADE": "pregao"}[name]

    with pytest.raises(ValueError, match="LEGADO_MODALIDADE expected digits"):
        legado_modalidades(Path(".env"), load_secret)


def test_item_licitacao_script_walks_modalidades_without_required_env() -> None:
    src = (
        Path(__file__).resolve().parents[1]
        / "etl/ingestion/legado/legado_item_licitacao.py"
    ).read_text(encoding="utf-8")
    assert "legado_modalidade(" not in src
    assert "legado_modalidades" in src
    assert "for modalidade in" in src


def test_legado_optional_uasg_returns_none_when_missing() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        raise KeyError(name)

    assert legado_optional_uasg(Path(".env"), load_secret) is None


def test_legado_optional_uasg_parses_int() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"LEGADO_UASG": "153001"}[name]

    assert legado_optional_uasg(Path(".env"), load_secret) == 153001

from pathlib import Path

import pytest

from etl.ingestion.planejamento.pgc_filters import (
    pgc_ano,
    pgc_optional_uasg,
    pgc_orgao_ano,
)


def test_pgc_orgao_ano_reads_env_values() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"PGC_ORGAO": "36000", "PGC_ANO": "2026"}[name]

    assert pgc_orgao_ano(Path(".env"), load_secret) == ("36000", 2026)


def test_pgc_orgao_ano_rejects_non_digit_year() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"PGC_ORGAO": "36000", "PGC_ANO": "twenty"}[name]

    with pytest.raises(ValueError, match="PGC_ANO expected digits, got 'twenty'"):
        pgc_orgao_ano(Path(".env"), load_secret)


def test_pgc_orgao_ano_rejects_year_outside_range() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"PGC_ORGAO": "36000", "PGC_ANO": "1999"}[name]

    with pytest.raises(ValueError, match="PGC_ANO expected year 2000-2100, got 1999"):
        pgc_orgao_ano(Path(".env"), load_secret)


def test_pgc_ano_reads_year_only() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"PGC_ANO": "2026"}[name]

    assert pgc_ano(Path(".env"), load_secret) == 2026


def test_pgc_optional_uasg_returns_none_when_missing() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        raise KeyError(name)

    assert pgc_optional_uasg(Path(".env"), load_secret) is None


def test_pgc_optional_uasg_returns_value_when_set() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"PGC_CODIGO_UASG": "153001"}[name]

    assert pgc_optional_uasg(Path(".env"), load_secret) == "153001"

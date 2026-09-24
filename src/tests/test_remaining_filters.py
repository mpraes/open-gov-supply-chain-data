from datetime import date
from pathlib import Path

import pytest

from etl.ingestion.remaining_filters import (
    PNCP_CONTRATACAO_MODALIDADES,
    alice_datetimes,
    arp_ata_header,
    arp_ata_keys,
    arp_dates,
    contratacoes_dates,
    contratacoes_modalidades,
    contratos_orgao_dates,
)


def test_contratacoes_dates_reads_env() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {
            "CONTRATACOES_DATA_INICIAL": "2024-01-01",
            "CONTRATACOES_DATA_FINAL": "2024-12-31",
        }[name]

    assert contratacoes_dates(Path(".env"), load_secret) == (
        "2024-01-01",
        "2024-12-31",
    )


def test_contratacoes_dates_defaults_to_full_window_when_env_missing() -> None:
    assert contratacoes_dates(Path(".env"), _missing_secret, today=date(2026, 9, 22)) == (
        "2000-01-01",
        "2026-09-22",
    )


def test_contratacoes_modalidades_reads_env() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {"CONTRATACOES_MODALIDADE": "6"}[name]

    assert contratacoes_modalidades(Path(".env"), load_secret) == (6,)


def test_contratacoes_modalidades_defaults_to_all_pncp_codes_when_missing() -> None:
    assert contratacoes_modalidades(Path(".env"), _missing_secret) == (
        PNCP_CONTRATACAO_MODALIDADES
    )
    assert PNCP_CONTRATACAO_MODALIDADES == tuple(range(1, 14))


def test_contratacoes_modalidades_rejects_non_digits() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return "pregao"

    with pytest.raises(ValueError, match="CONTRATACOES_MODALIDADE expected digits"):
        contratacoes_modalidades(Path(".env"), load_secret)


def test_contratos_orgao_dates_reads_env() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {
            "CONTRATOS_ORGAO": "36000",
            "CONTRATOS_DATA_INICIAL": "2024-01-01",
            "CONTRATOS_DATA_FINAL": "2024-06-30",
        }[name]

    assert contratos_orgao_dates(Path(".env"), load_secret) == (
        "36000",
        "2024-01-01",
        "2024-06-30",
    )


def test_arp_ata_keys_reads_three_values() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {
            "ARP_NUMERO_ATA": "1",
            "ARP_UNIDADE_GERENCIADORA": "153001",
            "ARP_NUMERO_ITEM": "2",
        }[name]

    assert arp_ata_keys(Path(".env"), load_secret) == ("1", "153001", "2")


def _missing_secret(_env_path: Path, name: str) -> str:
    raise KeyError(name)


def test_arp_dates_reads_env_when_present() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {
            "ARP_DATA_INICIAL": "2024-01-01",
            "ARP_DATA_FINAL": "2024-06-30",
        }[name]

    assert arp_dates(Path(".env"), load_secret) == ("2024-01-01", "2024-06-30")


def test_arp_dates_defaults_to_full_window_when_env_missing() -> None:
    assert arp_dates(Path(".env"), _missing_secret, today=date(2026, 9, 22)) == (
        "2000-01-01",
        "2026-09-22",
    )


def test_alice_datetimes_reads_env_when_present() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {
            "ALICE_DATA_INICIAL": "01/01/2024 00:00:00",
            "ALICE_DATA_FINAL": "31/01/2024 23:59:59",
        }[name]

    assert alice_datetimes(Path(".env"), load_secret) == (
        "01/01/2024 00:00:00",
        "31/01/2024 23:59:59",
    )


def test_alice_datetimes_defaults_to_full_window_when_env_missing() -> None:
    assert alice_datetimes(Path(".env"), _missing_secret, today=date(2026, 9, 22)) == (
        "01/01/2000 00:00:00",
        "22/09/2026 23:59:59",
    )


def test_arp_ata_header_missing_is_none() -> None:
    assert arp_ata_header(Path(".env"), _missing_secret) is None


def test_arp_ata_keys_missing_is_none() -> None:
    assert arp_ata_keys(Path(".env"), _missing_secret) is None

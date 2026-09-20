from pathlib import Path

from etl.ingestion.remaining_filters import (
    arp_ata_keys,
    contratacoes_date_modalidade,
    contratos_orgao_dates,
)


def test_contratacoes_date_modalidade_reads_env() -> None:
    def load_secret(_env_path: Path, name: str) -> str:
        return {
            "CONTRATACOES_DATA_INICIAL": "2024-01-01",
            "CONTRATACOES_DATA_FINAL": "2024-12-31",
            "CONTRATACOES_MODALIDADE": "6",
        }[name]

    assert contratacoes_date_modalidade(Path(".env"), load_secret) == (
        "2024-01-01",
        "2024-12-31",
        6,
    )


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

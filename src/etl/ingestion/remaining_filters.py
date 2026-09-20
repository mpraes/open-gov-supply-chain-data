from pathlib import Path

from etl.ingestion.env_filters import (
    require_int_value,
    require_iso_date_pair,
    require_text,
)
from etl.ingestion.script_runner import LoadSecret


def contratacoes_date_modalidade(
    env_path: Path, load_secret: LoadSecret
) -> tuple[str, str, int]:
    """Load CONTRATACOES_DATA_* and CONTRATACOES_MODALIDADE."""
    inicial, final = require_iso_date_pair(
        env_path, load_secret, "CONTRATACOES_DATA_INICIAL", "CONTRATACOES_DATA_FINAL"
    )
    return inicial, final, require_int_value(env_path, load_secret, "CONTRATACOES_MODALIDADE")


def contratacoes_dates(env_path: Path, load_secret: LoadSecret) -> tuple[str, str]:
    """Load CONTRATACOES_DATA_INICIAL and CONTRATACOES_DATA_FINAL."""
    return require_iso_date_pair(
        env_path, load_secret, "CONTRATACOES_DATA_INICIAL", "CONTRATACOES_DATA_FINAL"
    )


def arp_dates(env_path: Path, load_secret: LoadSecret) -> tuple[str, str]:
    """Load ARP_DATA_INICIAL and ARP_DATA_FINAL."""
    return require_iso_date_pair(env_path, load_secret, "ARP_DATA_INICIAL", "ARP_DATA_FINAL")


def arp_ata_header(env_path: Path, load_secret: LoadSecret) -> tuple[str, str]:
    """Load ARP_NUMERO_ATA and ARP_UNIDADE_GERENCIADORA."""
    return (
        require_text(env_path, load_secret, "ARP_NUMERO_ATA"),
        require_text(env_path, load_secret, "ARP_UNIDADE_GERENCIADORA"),
    )


def arp_ata_keys(env_path: Path, load_secret: LoadSecret) -> tuple[str, str, str]:
    """Load ARP_NUMERO_ATA, ARP_UNIDADE_GERENCIADORA and ARP_NUMERO_ITEM."""
    ata, unidade = arp_ata_header(env_path, load_secret)
    return ata, unidade, require_text(env_path, load_secret, "ARP_NUMERO_ITEM")


def contratos_orgao_dates(
    env_path: Path, load_secret: LoadSecret
) -> tuple[str, str, str]:
    """Load CONTRATOS_ORGAO and CONTRATOS_DATA_*."""
    orgao = require_text(env_path, load_secret, "CONTRATOS_ORGAO")
    inicial, final = require_iso_date_pair(
        env_path, load_secret, "CONTRATOS_DATA_INICIAL", "CONTRATOS_DATA_FINAL"
    )
    return orgao, inicial, final


def ocds_buyer_dates(env_path: Path, load_secret: LoadSecret) -> tuple[str, str, str]:
    """Load OCDS_BUYER_ID and OCDS_DATA_*."""
    buyer = require_text(env_path, load_secret, "OCDS_BUYER_ID")
    inicial, final = require_iso_date_pair(
        env_path, load_secret, "OCDS_DATA_INICIAL", "OCDS_DATA_FINAL"
    )
    return buyer, inicial, final


def indicadores_ano(env_path: Path, load_secret: LoadSecret) -> int:
    """Load INDICADORES_ANO."""
    return require_int_value(env_path, load_secret, "INDICADORES_ANO")


def alice_datetimes(env_path: Path, load_secret: LoadSecret) -> tuple[str, str]:
    """Load ALICE_DATA_INICIAL and ALICE_DATA_FINAL as DD/MM/YYYY HH:MM:SS."""
    inicial = require_text(env_path, load_secret, "ALICE_DATA_INICIAL")
    final = require_text(env_path, load_secret, "ALICE_DATA_FINAL")
    return inicial, final

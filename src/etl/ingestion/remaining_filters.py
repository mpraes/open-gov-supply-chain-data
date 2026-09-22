from datetime import date
from pathlib import Path

from etl.ingestion.env_filters import (
    default_iso_date_pair,
    optional_iso_date_pair,
    optional_text,
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


def arp_dates(
    env_path: Path, load_secret: LoadSecret, *, today: date | None = None
) -> tuple[str, str]:
    """Load ARP_DATA_* or a full dump window when both keys are missing.

    Example:
        arp_dates(Path(".env"), load)
    """
    pair = optional_iso_date_pair(
        env_path, load_secret, "ARP_DATA_INICIAL", "ARP_DATA_FINAL"
    )
    if pair is not None:
        return pair
    return default_iso_date_pair(today=today)


def arp_ata_header(env_path: Path, load_secret: LoadSecret) -> tuple[str, str] | None:
    """Load ARP ATA header keys, or None when both are missing.

    Example:
        arp_ata_header(Path(".env"), load)
    """
    ata = optional_text(env_path, load_secret, "ARP_NUMERO_ATA")
    unidade = optional_text(env_path, load_secret, "ARP_UNIDADE_GERENCIADORA")
    return _optional_pair(ata, unidade, "ARP_NUMERO_ATA", "ARP_UNIDADE_GERENCIADORA")


def arp_ata_keys(
    env_path: Path, load_secret: LoadSecret
) -> tuple[str, str, str] | None:
    """Load ARP ATA item keys, or None when all three are missing.

    Example:
        arp_ata_keys(Path(".env"), load)
    """
    header = arp_ata_header(env_path, load_secret)
    item = optional_text(env_path, load_secret, "ARP_NUMERO_ITEM")
    if header is None and item is None:
        return None
    if header is None or item is None:
        raise ValueError(
            f"expected ARP ATA header and ARP_NUMERO_ITEM together, got {header!r} and {item!r}"
        )
    return header[0], header[1], item


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


def alice_datetimes(
    env_path: Path, load_secret: LoadSecret, *, today: date | None = None
) -> tuple[str, str]:
    """Load ALICE_DATA_* or a full dump window when both keys are missing.

    Example:
        alice_datetimes(Path(".env"), load)
    """
    inicial = optional_text(env_path, load_secret, "ALICE_DATA_INICIAL")
    final = optional_text(env_path, load_secret, "ALICE_DATA_FINAL")
    if inicial is None and final is None:
        return _alice_full_window(today)
    if inicial is None or final is None:
        raise ValueError(
            "expected both ALICE_DATA_INICIAL and ALICE_DATA_FINAL or neither, "
            f"got {inicial!r} and {final!r}"
        )
    return inicial, final


def _optional_pair(
    left: str | None, right: str | None, left_key: str, right_key: str
) -> tuple[str, str] | None:
    if left is None and right is None:
        return None
    if left is None or right is None:
        raise ValueError(
            f"expected both {left_key} and {right_key} or neither, got {left!r} and {right!r}"
        )
    return left, right


def _alice_full_window(today: date | None) -> tuple[str, str]:
    day = today if today is not None else date.today()
    return "01/01/2000 00:00:00", f"{day.strftime('%d/%m/%Y')} 23:59:59"

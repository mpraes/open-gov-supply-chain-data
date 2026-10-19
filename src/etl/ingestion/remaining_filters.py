from datetime import date
from pathlib import Path

from etl.ingestion.env_filters import optional_text
from etl.ingestion.full_dump import full_dump_dates
from etl.ingestion.script_runner import LoadSecret

PNCP_CONTRATACAO_MODALIDADES: tuple[int, ...] = tuple(range(1, 14))


def contratacoes_dates(
    env_path: Path, load_secret: LoadSecret, *, today: date | None = None
) -> tuple[str, str]:
    """Full contratação window. Date keys in the env file are not applied.

    Example:
        contratacoes_dates(Path(".env"), load, today=date(2026, 9, 22))
    """
    del env_path, load_secret
    return full_dump_dates(today=today)


def contratacoes_modalidades(
    env_path: Path, load_secret: LoadSecret
) -> tuple[int, ...]:
    """Every PNCP modalidade. A single CONTRATACOES_MODALIDADE key is not applied.

    Example:
        contratacoes_modalidades(Path(".env"), load) == tuple(range(1, 14))
    """
    del env_path, load_secret
    return PNCP_CONTRATACAO_MODALIDADES


def arp_dates(
    env_path: Path, load_secret: LoadSecret, *, today: date | None = None
) -> tuple[str, str]:
    """Full ARP window. Date keys in the env file are not applied.

    Example:
        arp_dates(Path(".env"), load, today=date(2026, 9, 22))
    """
    del env_path, load_secret
    return full_dump_dates(today=today)


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


def alice_datetimes(
    env_path: Path, load_secret: LoadSecret, *, today: date | None = None
) -> tuple[str, str]:
    """Full Alice window. Datetime keys in the env file are not applied.

    Example:
        alice_datetimes(Path(".env"), load, today=date(2026, 9, 22))
    """
    del env_path, load_secret
    return _alice_full_window(today)


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

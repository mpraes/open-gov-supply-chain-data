"""Monta as janelas e chaves de filtro das cargas de contratação, ARP e Alice."""

from datetime import date
from pathlib import Path

from etl.ingestion.env_filters import optional_text
from etl.ingestion.full_dump import full_dump_dates
from etl.ingestion.script_runner import LoadSecret

PNCP_CONTRATACAO_MODALIDADES: tuple[int, ...] = tuple(range(1, 14))


def contratacoes_dates(
    env_path: Path, load_secret: LoadSecret, *, today: date | None = None
) -> tuple[str, str]:
    """Janela completa de contratação. As chaves de data no arquivo de ambiente não são aplicadas.

    Exemplo:
        contratacoes_dates(Path(".env"), load, today=date(2026, 9, 22))
    """
    del env_path, load_secret
    return full_dump_dates(today=today)


def contratacoes_modalidades(
    env_path: Path, load_secret: LoadSecret
) -> tuple[int, ...]:
    """Todas as modalidades do PNCP. A chave CONTRATACOES_MODALIDADE no arquivo de ambiente não é aplicada.

    Exemplo:
        contratacoes_modalidades(Path(".env"), load) == tuple(range(1, 14))
    """
    del env_path, load_secret
    return PNCP_CONTRATACAO_MODALIDADES


def arp_dates(
    env_path: Path, load_secret: LoadSecret, *, today: date | None = None
) -> tuple[str, str]:
    """Janela completa de ARP. As chaves de data no arquivo de ambiente não são aplicadas.

    Exemplo:
        arp_dates(Path(".env"), load, today=date(2026, 9, 22))
    """
    del env_path, load_secret
    return full_dump_dates(today=today)


def arp_ata_header(env_path: Path, load_secret: LoadSecret) -> tuple[str, str] | None:
    """Carrega as chaves de cabeçalho da ATA da ARP, ou None quando as duas estão ausentes.

    Exemplo:
        arp_ata_header(Path(".env"), load)
    """
    ata = optional_text(env_path, load_secret, "ARP_NUMERO_ATA")
    unidade = optional_text(env_path, load_secret, "ARP_UNIDADE_GERENCIADORA")
    return _optional_pair(ata, unidade, "ARP_NUMERO_ATA", "ARP_UNIDADE_GERENCIADORA")


def arp_ata_keys(
    env_path: Path, load_secret: LoadSecret
) -> tuple[str, str, str] | None:
    """Carrega as chaves de item da ATA da ARP, ou None quando as três estão ausentes.

    Exemplo:
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
    """Janela completa do Alice. As chaves de data e hora no arquivo de ambiente não são aplicadas.

    Exemplo:
        alice_datetimes(Path(".env"), load, today=date(2026, 9, 22))
    """
    del env_path, load_secret
    return _alice_full_window(today)


def _optional_pair(
    left: str | None, right: str | None, left_key: str, right_key: str
) -> tuple[str, str] | None:
    """Devolve o par quando os dois valores existem, None quando os dois faltam, e recusa só um lado."""
    if left is None and right is None:
        return None
    if left is None or right is None:
        raise ValueError(
            f"expected both {left_key} and {right_key} or neither, got {left!r} and {right!r}"
        )
    return left, right


def _alice_full_window(today: date | None) -> tuple[str, str]:
    """Monta a janela de 01/01/2000 00:00:00 até 23:59:59 de today."""
    day = today if today is not None else date.today()
    return "01/01/2000 00:00:00", f"{day.strftime('%d/%m/%Y')} 23:59:59"

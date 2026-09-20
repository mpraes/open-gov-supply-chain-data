from datetime import date
from pathlib import Path

from etl.ingestion.script_runner import LoadSecret


def legado_date_range(env_path: Path, load_secret: LoadSecret) -> tuple[str, str]:
    """Load required LEGADO_DATA_INICIAL and LEGADO_DATA_FINAL.

    Example:
        inicial, final = legado_date_range(Path(".env"), load_secret)
    """
    inicial = _require_iso_date(
        load_secret(env_path, "LEGADO_DATA_INICIAL"), "LEGADO_DATA_INICIAL"
    )
    final = _require_iso_date(
        load_secret(env_path, "LEGADO_DATA_FINAL"), "LEGADO_DATA_FINAL"
    )
    return inicial, final


def legado_ano(env_path: Path, load_secret: LoadSecret) -> int:
    """Load required LEGADO_ANO from the env file.

    Example:
        ano = legado_ano(Path(".env"), load_secret)
    """
    return _require_ano(load_secret(env_path, "LEGADO_ANO"), "LEGADO_ANO")


def legado_modalidade(env_path: Path, load_secret: LoadSecret) -> int:
    """Load required LEGADO_MODALIDADE from the env file.

    Example:
        modalidade = legado_modalidade(Path(".env"), load_secret)
    """
    return _require_int(load_secret(env_path, "LEGADO_MODALIDADE"), "LEGADO_MODALIDADE")


def legado_optional_uasg(env_path: Path, load_secret: LoadSecret) -> int | None:
    """Load optional LEGADO_UASG; missing or blank becomes None.

    Example:
        uasg = legado_optional_uasg(Path(".env"), load_secret)
    """
    try:
        value = load_secret(env_path, "LEGADO_UASG")
    except KeyError:
        return None
    if not value.strip():
        return None
    return _require_int(value, "LEGADO_UASG")


def _require_iso_date(raw: str, label: str) -> str:
    try:
        date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"{label} expected YYYY-MM-DD, got {raw!r}") from exc
    return raw


def _require_ano(raw: str, label: str) -> int:
    ano = _require_int(raw, label)
    if ano < 2000 or ano > 2100:
        raise ValueError(f"{label} expected year 2000-2100, got {ano}")
    return ano


def _require_int(raw: str, label: str) -> int:
    if not raw.isdigit():
        raise ValueError(f"{label} expected digits, got {raw!r}")
    return int(raw)

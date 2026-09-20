from datetime import date
from pathlib import Path

from etl.ingestion.script_runner import LoadSecret


def require_iso_date_pair(
    env_path: Path,
    load_secret: LoadSecret,
    inicial_key: str,
    final_key: str,
) -> tuple[str, str]:
    """Load a required YYYY-MM-DD pair from the env file.

    Example:
        require_iso_date_pair(Path(".env"), load, "A", "B")
    """
    inicial = _require_iso_date(load_secret(env_path, inicial_key), inicial_key)
    final = _require_iso_date(load_secret(env_path, final_key), final_key)
    return inicial, final


def require_int_value(env_path: Path, load_secret: LoadSecret, key: str) -> int:
    """Load a required integer env value.

    Example:
        require_int_value(Path(".env"), load, "MOD")
    """
    raw = load_secret(env_path, key)
    if not raw.isdigit():
        raise ValueError(f"{key} expected digits, got {raw!r}")
    return int(raw)


def require_text(env_path: Path, load_secret: LoadSecret, key: str) -> str:
    """Load a required non-empty env string.

    Example:
        require_text(Path(".env"), load, "ORGAO")
    """
    value = load_secret(env_path, key).strip()
    if not value:
        raise ValueError(f"{key} must be non-empty, got {value!r}")
    return value


def optional_text(env_path: Path, load_secret: LoadSecret, key: str) -> str | None:
    """Load an optional env string; missing or blank becomes None.

    Example:
        optional_text(Path(".env"), load, "UASG")
    """
    try:
        value = load_secret(env_path, key)
    except KeyError:
        return None
    cleaned = value.strip()
    if not cleaned:
        return None
    return cleaned


def _require_iso_date(raw: str, label: str) -> str:
    try:
        date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"{label} expected YYYY-MM-DD, got {raw!r}") from exc
    return raw

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


def optional_iso_date_pair(
    env_path: Path,
    load_secret: LoadSecret,
    inicial_key: str,
    final_key: str,
) -> tuple[str, str] | None:
    """Load an optional YYYY-MM-DD pair; both missing becomes None.

    Example:
        optional_iso_date_pair(Path(".env"), load, "A", "B")
    """
    inicial = optional_text(env_path, load_secret, inicial_key)
    final = optional_text(env_path, load_secret, final_key)
    if inicial is None and final is None:
        return None
    if inicial is None or final is None:
        raise ValueError(
            f"expected both {inicial_key} and {final_key} or neither, "
            f"got {inicial!r} and {final!r}"
        )
    return _require_iso_date(inicial, inicial_key), _require_iso_date(final, final_key)


def default_iso_date_pair(*, today: date | None = None) -> tuple[str, str]:
    """Full ISO dump window from 2000-01-01 through `today`.

    Example:
        default_iso_date_pair(today=date(2026, 9, 22))
    """
    day = today if today is not None else date.today()
    return "2000-01-01", day.isoformat()


def _require_iso_date(raw: str, label: str) -> str:
    try:
        date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"{label} expected YYYY-MM-DD, got {raw!r}") from exc
    return raw

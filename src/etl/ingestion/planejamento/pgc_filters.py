from pathlib import Path

from etl.ingestion.script_runner import LoadSecret


def pgc_orgao_ano(env_path: Path, load_secret: LoadSecret) -> tuple[str, int]:
    """Load required PGC_ORGAO and PGC_ANO from the env file.

    Example:
        orgao, ano = pgc_orgao_ano(Path(".env"), load_secret)
    """
    orgao = load_secret(env_path, "PGC_ORGAO")
    return orgao, pgc_ano(env_path, load_secret)


def pgc_ano(env_path: Path, load_secret: LoadSecret) -> int:
    """Load required PGC_ANO from the env file.

    Example:
        ano = pgc_ano(Path(".env"), load_secret)
    """
    return _require_ano(load_secret(env_path, "PGC_ANO"))


def pgc_optional_uasg(env_path: Path, load_secret: LoadSecret) -> str | None:
    """Load optional PGC_CODIGO_UASG; missing or blank becomes None.

    Example:
        uasg = pgc_optional_uasg(Path(".env"), load_secret)
    """
    try:
        value = load_secret(env_path, "PGC_CODIGO_UASG")
    except KeyError:
        return None
    return value


def _require_ano(raw: str) -> int:
    if not raw.isdigit():
        raise ValueError(f"PGC_ANO expected digits, got {raw!r}")
    ano = int(raw)
    if ano < 2000 or ano > 2100:
        raise ValueError(f"PGC_ANO expected year 2000-2100, got {ano}")
    return ano

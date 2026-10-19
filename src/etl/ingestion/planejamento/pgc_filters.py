"""Carrega PGC_ORGAO, PGC_ANO e PGC_CODIGO_UASG do arquivo de ambiente."""

from pathlib import Path

from etl.ingestion.script_runner import LoadSecret


def pgc_orgao_ano(env_path: Path, load_secret: LoadSecret) -> tuple[str, int]:
    """Carrega PGC_ORGAO e PGC_ANO obrigatórios do arquivo de ambiente.

    Exemplo:
        orgao, ano = pgc_orgao_ano(Path(".env"), load_secret)
    """
    orgao = load_secret(env_path, "PGC_ORGAO")
    return orgao, pgc_ano(env_path, load_secret)


def pgc_ano(env_path: Path, load_secret: LoadSecret) -> int:
    """Carrega PGC_ANO obrigatório do arquivo de ambiente.

    Exemplo:
        ano = pgc_ano(Path(".env"), load_secret)
    """
    return _require_ano(load_secret(env_path, "PGC_ANO"))


def pgc_optional_uasg(env_path: Path, load_secret: LoadSecret) -> str | None:
    """Carrega PGC_CODIGO_UASG opcional; ausente ou em branco vira None.

    Exemplo:
        uasg = pgc_optional_uasg(Path(".env"), load_secret)
    """
    try:
        value = load_secret(env_path, "PGC_CODIGO_UASG")
    except KeyError:
        return None
    return value


def _require_ano(raw: str) -> int:
    """Exige dígitos e um ano entre 2000 e 2100 em PGC_ANO."""
    if not raw.isdigit():
        raise ValueError(f"PGC_ANO expected digits, got {raw!r}")
    ano = int(raw)
    if ano < 2000 or ano > 2100:
        raise ValueError(f"PGC_ANO expected year 2000-2100, got {ano}")
    return ano

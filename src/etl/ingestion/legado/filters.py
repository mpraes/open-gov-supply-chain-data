"""Carrega as datas, o ano, a modalidade e a UASG opcional do módulo legado."""

from datetime import date
from pathlib import Path

from etl.ingestion.env_filters import optional_text
from etl.ingestion.script_runner import LoadSecret

# consultarItemLicitacao recusa a chamada sem modalidade. Estes códigos
# SIASG devolvem linhas: 1 Convite, 2 Tomada de Preços, 3 Concorrência,
# 4 Concorrência Internacional, 5 Pregão, 6 Dispensa, 7 Inexigibilidade,
# 20 Concurso.
LEGADO_ITEM_MODALIDADES: tuple[int, ...] = (1, 2, 3, 4, 5, 6, 7, 20)


def legado_date_range(env_path: Path, load_secret: LoadSecret) -> tuple[str, str]:
    """Carrega LEGADO_DATA_INICIAL e LEGADO_DATA_FINAL obrigatórios.

    Exemplo:
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
    """Carrega LEGADO_ANO obrigatório do arquivo de ambiente.

    Exemplo:
        ano = legado_ano(Path(".env"), load_secret)
    """
    return _require_ano(load_secret(env_path, "LEGADO_ANO"), "LEGADO_ANO")


def legado_modalidades(
    env_path: Path, load_secret: LoadSecret
) -> tuple[int, ...]:
    """Carrega LEGADO_MODALIDADE ou, se ausente, todos os códigos de modalidade de licitação do SIASG.

    Exemplo:
        legado_modalidades(Path(".env"), load_secret)
    """
    raw = optional_text(env_path, load_secret, "LEGADO_MODALIDADE")
    if raw is None:
        return LEGADO_ITEM_MODALIDADES
    return (_require_int(raw, "LEGADO_MODALIDADE"),)


def legado_optional_uasg(env_path: Path, load_secret: LoadSecret) -> int | None:
    """Carrega LEGADO_UASG opcional; ausente ou em branco vira None.

    Exemplo:
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
    """Exige uma data YYYY-MM-DD e retorna o texto recebido."""
    try:
        date.fromisoformat(raw)
    except ValueError as exc:
        raise ValueError(f"{label} expected YYYY-MM-DD, got {raw!r}") from exc
    return raw


def _require_ano(raw: str, label: str) -> int:
    """Exige um ano entre 2000 e 2100 e retorna o inteiro."""
    ano = _require_int(raw, label)
    if ano < 2000 or ano > 2100:
        raise ValueError(f"{label} expected year 2000-2100, got {ano}")
    return ano


def _require_int(raw: str, label: str) -> int:
    """Exige um texto só de dígitos e retorna o inteiro."""
    if not raw.isdigit():
        raise ValueError(f"{label} expected digits, got {raw!r}")
    return int(raw)

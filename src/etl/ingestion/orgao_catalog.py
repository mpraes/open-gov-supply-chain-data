"""Lê códigos de órgão e CNPJs de comprador já gravados em uasg_orgao."""

from pathlib import Path
from typing import Any

from config.load_secret_key import load_secret_key_func
from etl.ingestion.dest_schema import dest_table
from etl.ingestion.precos.catalog_codes import list_int_column
from etl.ingestion.script_runner import (
    DEFAULT_ENV_PATH,
    ConnectPostgresFn,
    LoadSecret,
    _open_connection,
)

_CNPJ_LENGTH = 14


def read_orgao_codes(
    *,
    env_path: Path = DEFAULT_ENV_PATH,
    load_secret: LoadSecret = load_secret_key_func,
    connect_fn: ConnectPostgresFn | None = None,
) -> list[int]:
    """Retorna cada `uasg_orgao.codigo_orgao`, ou falha se a tabela estiver vazia.

    Exemplo:
        read_orgao_codes() == [36000]
    """
    conn = _open_connection(env_path, load_secret, connect_fn)
    try:
        return _codes_or_raise(list_int_column(conn, _orgao_sql()))
    finally:
        conn.close()


def read_buyer_cnpjs(
    *,
    env_path: Path = DEFAULT_ENV_PATH,
    load_secret: LoadSecret = load_secret_key_func,
    connect_fn: ConnectPostgresFn | None = None,
) -> list[str]:
    """Retorna os CNPJs de 14 dígitos distintos de `uasg_orgao`.

    Exemplo:
        read_buyer_cnpjs() == ["00394460000112"]
    """
    conn = _open_connection(env_path, load_secret, connect_fn)
    try:
        return _cnpjs_or_raise(_text_column(conn, _cnpj_sql()))
    finally:
        conn.close()


def _orgao_sql() -> str:
    """Monta SELECT codigo_orgao FROM uasg_orgao ORDER BY codigo_orgao."""
    return f"SELECT codigo_orgao FROM {dest_table('uasg_orgao')} ORDER BY codigo_orgao"


def _cnpj_sql() -> str:
    """Monta SELECT DISTINCT cnpj_cpf_orgao de uasg_orgao, ignorando nulos."""
    table = dest_table("uasg_orgao")
    return (
        "SELECT DISTINCT cnpj_cpf_orgao FROM "
        f"{table} WHERE cnpj_cpf_orgao IS NOT NULL ORDER BY cnpj_cpf_orgao"
    )


def _codes_or_raise(codes: list[int]) -> list[int]:
    """Devolve os códigos ou recusa a lista vazia de uasg_orgao.codigo_orgao."""
    if codes:
        return codes
    raise ValueError("uasg_orgao.codigo_orgao expected at least one row, got 0")


def _cnpjs_or_raise(raw: list[str]) -> list[str]:
    """Devolve os CNPJs de 14 dígitos ou recusa a lista sem nenhum."""
    buyers = _distinct_cnpjs(raw)
    if buyers:
        return buyers
    raise ValueError(
        "uasg_orgao.cnpj_cpf_orgao expected at least one 14-digit CNPJ, "
        f"got {raw!r}"
    )


def _distinct_cnpjs(raw: list[str]) -> list[str]:
    """Mantém os valores distintos cujos dígitos formam um CNPJ de 14 caracteres."""
    found: list[str] = []
    seen: set[str] = set()
    for value in raw:
        digits = "".join(char for char in value if char.isdigit())
        if len(digits) != _CNPJ_LENGTH or digits in seen:
            continue
        seen.add(digits)
        found.append(digits)
    return found


def _text_column(conn: Any, sql: str) -> list[str]:
    """Executa o SELECT e devolve a primeira coluna de cada linha como texto."""
    with conn.cursor() as cur:
        cur.execute(sql)
        rows = cur.fetchall()
    return [_require_text(row, index) for index, row in enumerate(rows)]


def _require_text(row: object, index: int) -> str:
    """Devolve o texto da única célula, ou string vazia quando o valor é None."""
    if not isinstance(row, (tuple, list)) or len(row) != 1:
        raise ValueError(f"expected text row[{index}] to be a 1-tuple, got {row!r}")
    value = row[0]
    if value is None:
        return ""
    if not isinstance(value, str):
        raise ValueError(
            f"expected text row[{index}][0] to be str, got {type(value).__name__}: {value!r}"
        )
    return value

from pathlib import Path

import pytest

from etl.ingestion.orgao_catalog import read_buyer_cnpjs, read_orgao_codes


class _Cursor:
    def __init__(self, rows: list[tuple[object, ...]]) -> None:
        self._rows = rows
        self.sql = ""

    def execute(self, sql: str, params: object = None) -> None:
        self.sql = sql

    def fetchall(self) -> list[tuple[object, ...]]:
        return self._rows

    def __enter__(self) -> "_Cursor":
        return self

    def __exit__(self, *_exc: object) -> bool:
        return False


class _Conn:
    def __init__(self, rows: list[tuple[object, ...]]) -> None:
        self.rows = rows
        self.closed = False
        self.cursor_obj = _Cursor(rows)

    def cursor(self) -> _Cursor:
        return self.cursor_obj

    def close(self) -> None:
        self.closed = True


def test_read_orgao_codes_returns_dest_codes() -> None:
    conn = _Conn([(10,), (36000,)])
    codes = read_orgao_codes(
        env_path=Path(".env"),
        load_secret=_secret,
        connect_fn=lambda **_kwargs: conn,
    )
    assert codes == [10, 36000]
    assert "uasg_orgao" in conn.cursor_obj.sql
    assert conn.closed is True


def test_read_orgao_codes_rejects_empty_catalog() -> None:
    conn = _Conn([])
    with pytest.raises(ValueError, match="codigo_orgao expected at least one row, got 0"):
        read_orgao_codes(
            env_path=Path(".env"),
            load_secret=_secret,
            connect_fn=lambda **_kwargs: conn,
        )


def test_read_buyer_cnpjs_keeps_distinct_14_digit_values() -> None:
    conn = _Conn(
        [
            ("00.394.460/0001-12",),
            ("00394460000112",),
            ("12345678901",),
            ("",),
            (None,),
        ]
    )
    buyers = read_buyer_cnpjs(
        env_path=Path(".env"),
        load_secret=_secret,
        connect_fn=lambda **_kwargs: conn,
    )
    assert buyers == ["00394460000112"]


def test_read_buyer_cnpjs_rejects_catalog_without_cnpj() -> None:
    conn = _Conn([("12345678901",)])
    with pytest.raises(ValueError, match="14-digit CNPJ"):
        read_buyer_cnpjs(
            env_path=Path(".env"),
            load_secret=_secret,
            connect_fn=lambda **_kwargs: conn,
        )


def _secret(_env_path: Path, name: str) -> str:
    return name

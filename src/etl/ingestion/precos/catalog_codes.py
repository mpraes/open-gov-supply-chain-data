import re
from typing import Any

_SQL_IDENT = re.compile(r"^[a-z][a-z0-9_]*$")


def list_int_column(
    conn: Any,
    sql: str,
    params: dict[str, int] | None = None,
) -> list[int]:
    """Return one integer column from a SQL query.

    Example:
        codes = list_int_column(conn, "SELECT cod_item FROM material_item")
    """
    with conn.cursor() as cur:
        if params is None:
            cur.execute(sql)
        else:
            cur.execute(sql, params)
        rows = cur.fetchall()
    return [_require_int_code(row, index) for index, row in enumerate(rows)]


def list_codes_after(
    conn: Any,
    *,
    table: str,
    column: str,
    last_code: int,
    limit: int,
) -> list[int]:
    """Return the next catalog codes after a watermark, in order.

    Example:
        codes = list_codes_after(
            conn, table="material_item", column="cod_item", last_code=10, limit=20
        )
    """
    safe_table = _require_sql_ident(table, "table")
    safe_column = _require_sql_ident(column, "column")
    sql = (
        f"SELECT {safe_column} FROM {safe_table} "
        f"WHERE {safe_column} > %(last_code)s "
        f"ORDER BY {safe_column} LIMIT %(limit)s"
    )
    return list_int_column(conn, sql, {"last_code": last_code, "limit": limit})


def _require_sql_ident(value: str, label: str) -> str:
    if _SQL_IDENT.fullmatch(value) is None:
        raise ValueError(f"{label} expected snake_case identifier, got {value!r}")
    return value


def _require_int_code(row: object, index: int) -> int:
    if not isinstance(row, (tuple, list)) or len(row) != 1:
        raise ValueError(
            f"expected catalog code row[{index}] to be a 1-tuple, got {row!r}"
        )
    code = row[0]
    if isinstance(code, bool) or not isinstance(code, int):
        raise ValueError(
            f"expected catalog code row[{index}][0] to be int, "
            f"got {type(code).__name__}: {code!r}"
        )
    return code

import re
from typing import Any

_SQL_IDENT = re.compile(r"^[a-z][a-z0-9_]*$")


def list_int_column(
    conn: Any,
    sql: str,
    params: dict[str, str | int] | None = None,
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


def list_codes_after_absent(
    conn: Any,
    *,
    table: str,
    column: str,
    last_code: int,
    limit: int,
    dest_table: str,
    dest_column: str,
    dest_filters: dict[str, str | int],
) -> list[int]:
    """Return catalog codes after a cursor that are missing from dest.

    Example:
        list_codes_after_absent(
            conn, table="material_class", column="cod_classe",
            last_code=0, limit=20, dest_table="pgc_detalhe_catalogo",
            dest_column="codigo_classe_material", dest_filters={"ano_artefato": 2026},
        )
    """
    sql, params = _absent_codes_sql(
        table, column, dest_table, dest_column, dest_filters, last_code, limit
    )
    return list_int_column(conn, sql, params)


def _absent_codes_sql(
    table: str,
    column: str,
    dest_table: str,
    dest_column: str,
    dest_filters: dict[str, str | int],
    last_code: int,
    limit: int,
) -> tuple[str, dict[str, str | int]]:
    src_table = _require_sql_ident(table, "table")
    src_col = _require_sql_ident(column, "column")
    dst_table = _require_sql_ident(dest_table, "dest_table")
    dst_col = _require_sql_ident(dest_column, "dest_column")
    filter_sql, params = _filter_clauses(dest_filters)
    sql = (
        f"SELECT {src_col} FROM {src_table} src "
        f"WHERE {src_col} > %(last_code)s AND NOT EXISTS ("
        f"SELECT 1 FROM {dst_table} dest WHERE dest.{dst_col} = src.{src_col}{filter_sql}"
        f") ORDER BY {src_col} LIMIT %(limit)s"
    )
    params["last_code"] = last_code
    params["limit"] = limit
    return sql, params


def _filter_clauses(dest_filters: dict[str, str | int]) -> tuple[str, dict[str, str | int]]:
    params: dict[str, str | int] = {}
    parts: list[str] = []
    for key, value in dest_filters.items():
        ident = _require_sql_ident(key, "dest_filters")
        parts.append(f" AND dest.{ident} = %({ident})s")
        params[ident] = value
    return "".join(parts), params


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

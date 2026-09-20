import re
from collections.abc import Mapping
from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Literal

from clients.compras_api import CodeParamsFn, QueryParams
from etl.ingestion.dest_schema import dest_table, require_sql_ident

_ISO_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})")
_ALICE_DT = "%d/%m/%Y %H:%M:%S"
WatermarkKind = Literal["iso", "alice"]
WhereClause = Mapping[str, str | int]


@dataclass(frozen=True)
class DateWatermark:
    """Dest MAX(date) used to raise an API start-date query param."""

    table: str
    column: str
    start_param: str
    end_param: str
    where: WhereClause | None = None
    kind: WatermarkKind = "iso"


def raise_date_window(
    env_inicial: str, env_final: str, dest_max: str | None
) -> tuple[str, str] | None:
    """Raise the API start date to dest max, overlapping the last loaded day.

    Example:
        raise_date_window("2024-01-01", "2024-12-31", "2024-06-15")
    """
    if dest_max is None:
        return env_inicial, env_final
    if dest_max > env_final:
        return None
    if dest_max < env_inicial:
        return env_inicial, env_final
    return dest_max, env_final


def iso_date_prefix(value: object) -> str | None:
    """Normalize a dest MAX value to YYYY-MM-DD.

    Example:
        iso_date_prefix("2024-06-15T10:30:00") == "2024-06-15"
    """
    if value is None:
        return None
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    if isinstance(value, str):
        return _iso_from_text(value)
    raise ValueError(
        f"expected dest MAX date as str/date/datetime, got {type(value).__name__}: {value!r}"
    )


def max_dest_iso_date(
    conn: Any,
    table: str,
    column: str,
    where: WhereClause | None = None,
) -> str | None:
    """Return MAX(column) from dest as YYYY-MM-DD, or None when empty.

    Example:
        max_dest_iso_date(conn, "contratacao", "data_publicacao_pncp")
    """
    sql, params = _max_sql(table, column, where)
    with conn.cursor() as cur:
        if params is None:
            cur.execute(sql)
        else:
            cur.execute(sql, params)
        row = cur.fetchone()
    return iso_date_prefix(_max_cell(row))


def apply_date_watermark(
    conn: Any,
    query_params: QueryParams,
    watermark: DateWatermark,
) -> dict[str, str | int | bool] | None:
    """Copy query params with a dest-raised start date, or None if caught up.

    Example:
        apply_date_watermark(conn, params, DateWatermark(...))
    """
    params = dict(query_params)
    inicial = _require_param_text(params, watermark.start_param)
    final = _require_param_text(params, watermark.end_param)
    window = _raised_param_window(conn, watermark, inicial, final)
    if window is None:
        return None
    params[watermark.start_param] = window[0]
    return params


def with_dest_compra_inicio(
    params_for_code: CodeParamsFn,
    conn: Any,
    table: str,
    code_column: str,
    *,
    stringify_code: bool = False,
    date_column: str = "data_compra",
) -> CodeParamsFn:
    """Add dataCompraInicio from dest MAX(date_column) for one catalog code.

    Example:
        with_dest_compra_inicio(params_fn, conn, "preco_material", "codigo_pdm")
    """

    def wrapped(code: int) -> dict[str, str | int | bool]:
        params = dict(params_for_code(code))
        dest_max = max_dest_iso_date(
            conn,
            table,
            date_column,
            {code_column: _code_where_value(code, stringify_code)},
        )
        if dest_max is not None:
            params["dataCompraInicio"] = dest_max
        return params

    return wrapped


def _code_where_value(code: int, stringify_code: bool) -> str | int:
    if stringify_code:
        return str(code)
    return code


def rewrite_job_slice(job_name: str, old_start: str, new_start: str) -> str:
    """Swap the original window start inside a slice job name.

    Example:
        rewrite_job_slice("contratacao:2024-01-01:2024-12-31", "2024-01-01", "2024-06-15")
    """
    return job_name.replace(old_start, new_start, 1)


def _raised_param_window(
    conn: Any,
    watermark: DateWatermark,
    inicial: str,
    final: str,
) -> tuple[str, str] | None:
    dest_iso = max_dest_iso_date(conn, watermark.table, watermark.column, watermark.where)
    if watermark.kind == "alice":
        return _raise_alice_window(inicial, final, dest_iso)
    return raise_date_window(inicial, final, dest_iso)


def _raise_alice_window(
    inicial: str, final: str, dest_iso: str | None
) -> tuple[str, str] | None:
    raised = raise_date_window(_alice_to_iso(inicial), _alice_to_iso(final), dest_iso)
    if raised is None:
        return None
    return _iso_to_alice_start(raised[0]), final


def _iso_from_text(raw: str) -> str | None:
    match = _ISO_PREFIX.match(raw)
    if match is not None:
        return _require_iso_date(match.group(1), raw)
    return _alice_to_iso(raw)


def _alice_to_iso(raw: str) -> str:
    try:
        return datetime.strptime(raw, _ALICE_DT).date().isoformat()
    except ValueError as exc:
        raise ValueError(
            f"expected Alice DD/MM/YYYY HH:MM:SS or ISO date, got {raw!r}"
        ) from exc


def _iso_to_alice_start(iso: str) -> str:
    parsed = date.fromisoformat(iso)
    return parsed.strftime("%d/%m/%Y") + " 00:00:00"


def _require_iso_date(iso: str, raw: str) -> str:
    try:
        date.fromisoformat(iso)
    except ValueError as exc:
        raise ValueError(f"expected ISO date prefix in {raw!r}, got {iso!r}") from exc
    return iso


def _max_sql(
    table: str, column: str, where: WhereClause | None
) -> tuple[str, dict[str, str | int] | None]:
    safe_column = require_sql_ident(column, "column")
    sql = f"SELECT MAX({safe_column}) FROM {dest_table(table)}"
    if where is None:
        return sql, None
    return _sql_with_where(sql, where)


def _sql_with_where(sql: str, where: WhereClause) -> tuple[str, dict[str, str | int]]:
    clauses: list[str] = []
    params: dict[str, str | int] = {}
    for key, value in where.items():
        ident = require_sql_ident(key, "where")
        clauses.append(f"{ident} = %({ident})s")
        params[ident] = value
    return f"{sql} WHERE {' AND '.join(clauses)}", params


def _max_cell(row: object) -> object:
    if row is None:
        return None
    if not isinstance(row, (tuple, list)) or len(row) != 1:
        raise ValueError(f"expected dest MAX row to be a 1-tuple, got {row!r}")
    return row[0]


def _require_param_text(params: dict[str, str | int | bool], key: str) -> str:
    if key not in params:
        raise ValueError(f"query_params missing {key!r}, got {sorted(params)!r}")
    value = params[key]
    if not isinstance(value, str):
        raise ValueError(f"{key} expected str date, got {type(value).__name__}: {value!r}")
    return value



from typing import Any

from etl.ingestion.dest_schema import dest_table

_CURSOR_TABLE = dest_table("etl_code_cursor")

ENSURE_CURSOR_SQL = f"""
CREATE TABLE IF NOT EXISTS {_CURSOR_TABLE} (
job_name TEXT PRIMARY KEY,
last_code BIGINT NOT NULL,
updated_at TIMESTAMPTZ DEFAULT now()
);
"""

LOAD_CURSOR_SQL = f"""
SELECT last_code FROM {_CURSOR_TABLE} WHERE job_name = %(job_name)s;
"""

SAVE_CURSOR_SQL = f"""
INSERT INTO {_CURSOR_TABLE} (job_name, last_code)
VALUES (%(job_name)s, %(last_code)s)
ON CONFLICT (job_name) DO UPDATE SET
last_code = EXCLUDED.last_code,
updated_at = now();
"""


def ensure_job_cursor_table(conn: Any) -> None:
    """Create etl_code_cursor if the watermark table is missing.

    Example:
        ensure_job_cursor_table(conn)
    """
    with conn.cursor() as cur:
        cur.execute(ENSURE_CURSOR_SQL)
    conn.commit()


def load_job_cursor(conn: Any, job_name: str) -> int:
    """Return the last processed watermark, or 0 when unset.

    Example:
        last = load_job_cursor(conn, "material_item")
    """
    with conn.cursor() as cur:
        cur.execute(LOAD_CURSOR_SQL, {"job_name": job_name})
        row = cur.fetchone()
    return _cursor_last_value(row)


def save_job_cursor(conn: Any, job_name: str, last_value: int) -> None:
    """Persist a job watermark after a successful batch.

    Example:
        save_job_cursor(conn, "material_item", 3)
    """
    with conn.cursor() as cur:
        cur.execute(SAVE_CURSOR_SQL, {"job_name": job_name, "last_code": last_value})
    conn.commit()


def _cursor_last_value(row: object) -> int:
    if row is None:
        return 0
    if not isinstance(row, (tuple, list)) or len(row) != 1:
        raise ValueError(f"expected cursor row to be a 1-tuple, got {row!r}")
    value = row[0]
    if isinstance(value, bool) or not isinstance(value, int):
        raise ValueError(
            f"expected cursor last_code to be int, got {type(value).__name__}: {value!r}"
        )
    return value

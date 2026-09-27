from dashboard.db import AnalyticsConnection


def fetch_one_row(conn: AnalyticsConnection, query: str) -> tuple[object, ...] | None:
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchone()


def fetch_rows(conn: AnalyticsConnection, query: str) -> list[tuple[object, ...]]:
    cursor = conn.cursor()
    cursor.execute(query)
    return cursor.fetchall()

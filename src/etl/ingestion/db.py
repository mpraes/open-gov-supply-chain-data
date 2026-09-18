from collections.abc import Callable
from typing import Any

from psycopg2 import connect as psycopg2_connect

ConnectFn = Callable[..., Any]


def connect_postgres(
    *,
    host: str,
    port: str,
    user: str,
    password: str,
    dbname: str,
    connect_fn: ConnectFn = psycopg2_connect,
) -> Any:
    """Open a Postgres connection via an injectable connect function.

    Example:
        conn = connect_postgres(
            host=host, port=port, user=user, password=password, dbname=dbname
        )
    """
    return connect_fn(
        host=host,
        port=port,
        user=user,
        password=password,
        dbname=dbname,
    )

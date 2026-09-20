from etl.ingestion.db import connect_postgres


class FakePsycopgConnect:
    """Named fake that records connect kwargs and returns a sentinel connection."""

    def __init__(self) -> None:
        self.calls: list[dict[str, str]] = []
        self.connection = object()

    def __call__(
        self,
        *,
        host: str,
        port: str,
        user: str,
        password: str,
        dbname: str,
        options: str,
    ) -> object:
        self.calls.append(
            {
                "host": host,
                "port": port,
                "user": user,
                "password": password,
                "dbname": dbname,
                "options": options,
            }
        )
        return self.connection


def test_connect_postgres_forwards_kwargs_to_connect_fn() -> None:
    fake = FakePsycopgConnect()
    conn = connect_postgres(
        host="h",
        port="5432",
        user="u",
        password="p",
        dbname="d",
        connect_fn=fake,
    )
    assert conn is fake.connection
    assert fake.calls == [
        {
            "host": "h",
            "port": "5432",
            "user": "u",
            "password": "p",
            "dbname": "d",
            "options": "-c search_path=staging",
        }
    ]

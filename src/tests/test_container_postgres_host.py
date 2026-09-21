from etl.ingestion.container_postgres_host import container_postgres_host


def test_container_postgres_host_rewrites_loopback() -> None:
    assert container_postgres_host("localhost") == "host.docker.internal"
    assert container_postgres_host("127.0.0.1") == "host.docker.internal"


def test_container_postgres_host_keeps_remote_host() -> None:
    assert container_postgres_host("db.example.com") == "db.example.com"

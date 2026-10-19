"""Reescreve o host de loopback do Postgres para host.docker.internal."""


def container_postgres_host(host: str) -> str:
    """Reescreve hosts de loopback do banco para os workers Docker alcançarem o Postgres na máquina.

    Exemplo:
        container_postgres_host("localhost") == "host.docker.internal"
    """
    if host in {"localhost", "127.0.0.1"}:
        return "host.docker.internal"
    return host

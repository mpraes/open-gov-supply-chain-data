def container_postgres_host(host: str) -> str:
    """Rewrite loopback DB hosts so Docker workers reach Postgres on the machine.

    Example:
        container_postgres_host("localhost") == "host.docker.internal"
    """
    if host in {"localhost", "127.0.0.1"}:
        return "host.docker.internal"
    return host

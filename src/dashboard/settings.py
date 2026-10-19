"""Configuração de conexão Postgres lida do arquivo de ambiente do dashboard."""

from dataclasses import dataclass
from pathlib import Path

from config.load_secret_key import load_secret_key_func
from etl.ingestion.container_postgres_host import container_postgres_host


@dataclass(frozen=True)
class DashboardSettings:
    """Credenciais de conexão Postgres usadas pelo dashboard."""

    host: str
    port: str
    user: str
    password: str
    dbname: str


def load_dashboard_settings(env_path: Path) -> DashboardSettings:
    """Lê as variáveis PSQL_* de env_path e monta DashboardSettings, reescrevendo host de loopback."""
    host = container_postgres_host(load_secret_key_func(env_path, "PSQL_HOST"))
    return DashboardSettings(
        host=host,
        port=load_secret_key_func(env_path, "PSQL_PORT"),
        user=load_secret_key_func(env_path, "PSQL_USER"),
        password=load_secret_key_func(env_path, "PSQL_PASSWORD"),
        dbname=load_secret_key_func(env_path, "PSQL_DB"),
    )

import os
from pathlib import Path

import pytest

from dashboard.settings import load_dashboard_settings

_PSQL_ENV_KEYS = (
    "PSQL_HOST",
    "PSQL_PORT",
    "PSQL_USER",
    "PSQL_PASSWORD",
    "PSQL_DB",
)


@pytest.fixture(autouse=True)
def isolate_psql_env() -> None:
    """Prevent process PSQL_* from overriding tmp .env (load_secret_key override=False)."""
    saved = {key: os.environ.pop(key, None) for key in _PSQL_ENV_KEYS}
    yield
    for key, value in saved.items():
        if value is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = value


def test_load_dashboard_settings_reads_psql_keys_and_rewrites_localhost(
    tmp_path: Path,
) -> None:
    env_file = tmp_path / ".env"
    env_file.write_text(
        "\n".join(
            [
                "PSQL_HOST=localhost",
                "PSQL_PORT=5432",
                "PSQL_USER=homelab_postgres",
                "PSQL_PASSWORD=secret",
                "PSQL_DB=open_gov_supply_chain",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    settings = load_dashboard_settings(env_file)
    assert settings.host == "host.docker.internal"
    assert settings.port == "5432"
    assert settings.user == "homelab_postgres"
    assert settings.password == "secret"
    assert settings.dbname == "open_gov_supply_chain"

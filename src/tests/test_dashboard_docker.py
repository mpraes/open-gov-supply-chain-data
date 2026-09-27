from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DOCKERFILE = ROOT / "src/dashboard/Dockerfile"
COMPOSE = ROOT / "src/dashboard/compose.yml"


def test_dockerfile_runs_uvicorn_on_8050() -> None:
    text = DOCKERFILE.read_text(encoding="utf-8")
    assert "python:3.12-slim" in text
    assert "PYTHONPATH=src" in text
    assert "0.0.0.0" in text
    assert "8050" in text
    assert "dashboard.app:app" in text


def test_compose_publishes_8050_and_host_gateway() -> None:
    text = COMPOSE.read_text(encoding="utf-8")
    assert "8050:8050" in text
    assert "host.docker.internal:host-gateway" in text
    assert ".env" in text


def test_dockerfile_syncs_frozen_lockfile_without_env() -> None:
    text = DOCKERFILE.read_text(encoding="utf-8")
    assert "uv sync --frozen --no-dev" in text
    assert "COPY .env" not in text


def test_dockerignore_excludes_secrets_and_bulk() -> None:
    text = (ROOT / ".dockerignore").read_text(encoding="utf-8")
    for pattern in (".env", ".git", ".venv", "data/", "__pycache__", ".worktrees", ".superpowers"):
        assert pattern in text

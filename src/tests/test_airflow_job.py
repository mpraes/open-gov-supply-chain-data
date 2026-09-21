import os

from pytest import MonkeyPatch

from etl.ingestion.airflow_job import run_ingest_main, run_named_ingest


class FakeIngestMain:
    def __init__(self) -> None:
        self.calls = 0

    def __call__(self) -> None:
        self.calls += 1


class FakeIngestModule:
    def __init__(self) -> None:
        self.main = FakeIngestMain()


def test_run_ingest_main_rewrites_localhost_and_calls_job(monkeypatch: MonkeyPatch) -> None:
    monkeypatch.setenv("PSQL_HOST", "localhost")
    job = FakeIngestMain()
    run_ingest_main(job)
    assert job.calls == 1
    assert os.environ["PSQL_HOST"] == "host.docker.internal"


def test_run_named_ingest_imports_module_main(monkeypatch: MonkeyPatch) -> None:
    fake = FakeIngestModule()
    monkeypatch.setenv("PSQL_HOST", "db.internal")
    monkeypatch.setattr("importlib.import_module", lambda path: fake)
    run_named_ingest("etl.ingestion.material.material_group")
    assert fake.main.calls == 1
    assert os.environ["PSQL_HOST"] == "db.internal"

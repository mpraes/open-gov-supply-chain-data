from collections.abc import Callable
import importlib
import os

from dotenv import load_dotenv

from etl.ingestion.container_postgres_host import container_postgres_host
from etl.ingestion.script_runner import DEFAULT_ENV_PATH

IngestMain = Callable[[], None]


def run_ingest_main(main: IngestMain) -> None:
    """Run one ingest `main()`, rewriting loopback Postgres for Docker.

    Example:
        run_ingest_main(material_group.main)
    """
    load_dotenv(DEFAULT_ENV_PATH, override=False)
    os.environ["PSQL_HOST"] = container_postgres_host(
        os.getenv("PSQL_HOST", "localhost")
    )
    main()


def run_named_ingest(module_path: str) -> None:
    """Import `module_path.main` and run it via `run_ingest_main`.

    Example:
        run_named_ingest("etl.ingestion.material.material_group")
    """
    module = importlib.import_module(module_path)
    run_ingest_main(module.main)

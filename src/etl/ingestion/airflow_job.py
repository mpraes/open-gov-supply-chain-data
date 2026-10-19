"""Executa um main de ingestão a partir do Airflow, apontando o Postgres de loopback para o host Docker."""

from collections.abc import Callable
import importlib
import os

from dotenv import load_dotenv

from etl.ingestion.container_postgres_host import container_postgres_host
from etl.ingestion.script_runner import DEFAULT_ENV_PATH

IngestMain = Callable[[], None]


def run_ingest_main(main: IngestMain) -> None:
    """Executa um `main()` de ingestão, reescrevendo o Postgres de loopback para o Docker.

    Exemplo:
        run_ingest_main(material_group.main)
    """
    load_dotenv(DEFAULT_ENV_PATH, override=False)
    os.environ["PSQL_HOST"] = container_postgres_host(
        os.getenv("PSQL_HOST", "localhost")
    )
    main()


def run_named_ingest(module_path: str) -> None:
    """Importa `module_path.main` e executa via `run_ingest_main`.

    Exemplo:
        run_named_ingest("etl.ingestion.material.material_group")
    """
    module = importlib.import_module(module_path)
    run_ingest_main(module.main)

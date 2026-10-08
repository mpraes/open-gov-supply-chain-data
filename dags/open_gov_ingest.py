from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

from airflow.sdk import dag, task

from open_gov_schedule import every_two_days_at

_PROJECT_SRC = Path("/home/renan/personal/projects/open-gov-supply-chain-data/src")
_DEFAULT_START = datetime(2026, 1, 1, tzinfo=timezone.utc)


def register_ingest_dag(
    *,
    dag_id: str,
    module_path: str,
    tags: list[str],
    task_id: str,
    doc: str,
    schedule: str | timedelta | None = None,
    start_date: datetime | None = None,
    paused: bool = True,
) -> None:
    """Register one Airflow 3 DAG that runs `module_path.main`.

    Example:
        register_ingest_dag(
            dag_id="open_gov_material_group",
            module_path="etl.ingestion.material.material_group",
            tags=["open-gov", "catmat"],
            task_id="ingest_material_group",
            doc="Manual trigger for `1_consultarGrupoMaterial`.",
        )
    """

    @dag(
        dag_id=dag_id,
        schedule=schedule,
        start_date=start_date or _DEFAULT_START,
        catchup=False,
        max_active_runs=1,
        tags=tags,
        is_paused_upon_creation=paused,
    )
    def ingest_dag() -> None:
        ingest_dag.__doc__ = doc

        @task(task_id=task_id)
        def run_ingest() -> None:
            sys.path.insert(0, str(_PROJECT_SRC))
            from etl.ingestion.airflow_job import run_named_ingest

            run_named_ingest(module_path)

        run_ingest()

    ingest_dag()

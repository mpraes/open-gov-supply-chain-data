"""Registra DAGs Airflow para cada família de ingestão com um pool de API de uma vaga."""

from collections.abc import Sequence
from datetime import datetime, timedelta, timezone
from pathlib import Path
import sys

from airflow.sdk import Asset, dag, task

from open_gov_catalog import IngestStep

_PROJECT_SRC = Path("/home/renan/personal/projects/open-gov-supply-chain-data/src")
_DEFAULT_START = datetime(2026, 1, 1, tzinfo=timezone.utc)
# Criado fora da DAG (`airflow pools set`). O Airflow 3 bloqueia o ORM
# enquanto o dag processor importa este módulo.
API_POOL = "open_gov_compras_api"


def register_family_dag(
    *,
    dag_id: str,
    tags: list[str],
    doc: str,
    steps: Sequence[IngestStep],
    schedule: str | timedelta | None = None,
    start_date: datetime | None = None,
    paused: bool = True,
    schedule_assets: tuple[str, ...] = (),
    outlet_asset: str | None = None,
) -> None:
    """Registra a DAG de uma família. As tarefas de ingestão compartilham um pool de API com 1 vaga.

    Exemplo:
        register_family_dag(
            dag_id="open_gov_catmat",
            tags=["open-gov", "catmat"],
            doc="CATMAT in load order.",
            steps=CATMAT_STEPS,
        )
    """
    _require_known_upstream(steps)
    _declare_family(
        dag_id=dag_id,
        tags=tags,
        doc=doc,
        steps=steps,
        schedule=_family_schedule(schedule, schedule_assets),
        start_date=start_date or _DEFAULT_START,
        paused=paused,
        outlet_asset=outlet_asset,
    )


def _family_schedule(
    schedule: str | timedelta | None,
    schedule_assets: tuple[str, ...],
) -> str | timedelta | list[Asset] | None:
    """Recusa cron e assets juntos e devolve um dos dois como agenda da família."""
    if schedule_assets and schedule is not None:
        raise ValueError(
            "schedule and schedule_assets are exclusive, "
            f"got schedule={schedule!r} assets={schedule_assets!r}"
        )
    if not schedule_assets:
        return schedule
    return [Asset(name) for name in schedule_assets]


def _require_known_upstream(steps: Sequence[IngestStep]) -> None:
    """Exige que cada upstream aponte para um task_id da própria família."""
    known = {step.task_id for step in steps}
    for step in steps:
        _require_parents(step, known)


def _require_parents(step: IngestStep, known: set[str]) -> None:
    """Lança erro quando um upstream não é um task_id da família."""
    for parent in step.upstream:
        if parent not in known:
            raise ValueError(
                f"upstream expected a task_id in {sorted(known)!r}, got {parent!r}"
            )


def _declare_family(
    *,
    dag_id: str,
    tags: list[str],
    doc: str,
    steps: Sequence[IngestStep],
    schedule: str | timedelta | list[Asset] | None,
    start_date: datetime,
    paused: bool,
    outlet_asset: str | None,
) -> None:
    """Define a DAG da família e a chama para registrar as tarefas."""
    @dag(
        dag_id=dag_id,
        schedule=schedule,
        start_date=start_date,
        catchup=False,
        max_active_runs=1,
        max_active_tasks=1,
        tags=tags,
        is_paused_upon_creation=paused,
    )
    def family() -> None:
        """Monta as tarefas da família, liga os upstreams e publica o asset de saída."""
        family.__doc__ = doc
        bound = {step.task_id: _run_step(step) for step in steps}
        _wire_steps(bound, steps)
        if outlet_asset is not None:
            _publish(outlet_asset, _sink_tasks(bound, steps))

    family()


def _run_step(step: IngestStep) -> object:
    """Instancia a tarefa Airflow que executa o módulo de ingestão do passo."""
    module_path = step.module_path
    outlets = [Asset(step.outlet)] if step.outlet else None

    @task(task_id=step.task_id, pool=API_POOL, outlets=outlets)
    def run_ingest() -> None:
        """Insere o código do projeto no path e executa a ingestão nomeada."""
        sys.path.insert(0, str(_PROJECT_SRC))
        from etl.ingestion.airflow_job import run_named_ingest

        run_named_ingest(module_path)

    return run_ingest()


def _wire_steps(bound: dict[str, object], steps: Sequence[IngestStep]) -> None:
    """Encadeia cada tarefa com as predecessoras declaradas no passo."""
    for step in steps:
        for parent in step.upstream:
            bound[parent] >> bound[step.task_id]


def _sink_tasks(bound: dict[str, object], steps: Sequence[IngestStep]) -> list[object]:
    """Seleciona as tarefas que não aparecem como upstream de nenhum passo."""
    parents = {parent for step in steps for parent in step.upstream}
    return [bound[step.task_id] for step in steps if step.task_id not in parents]


def _publish(asset_name: str, parents: list[object]) -> None:
    """Cria a tarefa de prontidão e a liga às tarefas finais da família."""
    @task(task_id="publish_ready", outlets=[Asset(asset_name)])
    def publish_ready() -> None:
        """Publica o asset de prontidão e devolve None."""
        return None

    ready = publish_ready()
    for parent in parents:
        parent >> ready

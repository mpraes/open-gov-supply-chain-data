import inspect
from pathlib import Path
from typing import Any

from clients.compras_api import QueryParams
from etl.ingestion.page_runner import run_page_batch_ingestion
from etl.ingestion.remaining_run import (
    run_remaining_ingestion,
    run_sliced_remaining_ingestion,
)


class FakeRemainingIngest:
    def __init__(self) -> None:
        self.calls: list[dict[str, Any]] = []

    def __call__(self, **kwargs: Any) -> int:
        self.calls.append(kwargs)
        return 3


def _arp_params(inicial: str, final: str) -> QueryParams:
    return {"dataVigenciaInicialMin": inicial, "dataVigenciaInicialMax": final}


def test_remaining_ingestion_defaults_to_sequential_pages() -> None:
    remaining = inspect.signature(run_remaining_ingestion).parameters["parallel_pages"]
    runner = inspect.signature(run_page_batch_ingestion).parameters["parallel_pages"]
    assert remaining.default == 1
    assert runner.default == 1


def test_remaining_ingestion_forwards_parallel_pages() -> None:
    remaining_src = inspect.getsource(run_remaining_ingestion)
    assert "parallel_pages=parallel_pages" in remaining_src


def test_sliced_remaining_ingestion_runs_one_job_per_365_day_window() -> None:
    ingest = FakeRemainingIngest()
    count = run_sliced_remaining_ingestion(
        data_inicial="2024-01-01",
        data_final="2025-01-01",
        params_for_slice=_arp_params,
        job_prefix="arp",
        logger_name="arp",
        endpoint_path="/modulo-arp/1_consultarARP",
        table_name="arp",
        map_row=lambda row: row,
        run_one=ingest,
    )
    assert count == 6
    assert [call["job_name"] for call in ingest.calls] == [
        "arp:2024-01-01:2024-12-31",
        "arp:2025-01-01:2025-01-01",
    ]
    assert ingest.calls[0]["query_params"] == _arp_params("2024-01-01", "2024-12-31")


def test_sliced_remaining_ingestion_keeps_short_window_as_one_job() -> None:
    ingest = FakeRemainingIngest()
    run_sliced_remaining_ingestion(
        data_inicial="2026-01-01",
        data_final="2026-09-22",
        params_for_slice=_arp_params,
        job_prefix="arp",
        logger_name="arp",
        endpoint_path="/modulo-arp/1_consultarARP",
        table_name="arp",
        map_row=lambda row: row,
        run_one=ingest,
    )
    assert len(ingest.calls) == 1
    assert ingest.calls[0]["job_name"] == "arp:2026-01-01:2026-09-22"


def test_arp_date_window_scripts_slice_api_windows() -> None:
    root = Path(__file__).resolve().parents[1] / "etl/ingestion/arp"
    for name in ("arp.py", "arp_item.py", "arp_fim_vigencia.py"):
        src = (root / name).read_text(encoding="utf-8")
        assert "run_sliced_remaining_ingestion" in src
        assert "params_for_slice" in src


def test_contratacao_script_dumps_all_modalidades_without_required_env() -> None:
    src = (
        Path(__file__).resolve().parents[1]
        / "etl/ingestion/contratacoes/contratacao.py"
    ).read_text(encoding="utf-8")
    assert "contratacoes_date_modalidade" not in src
    assert "contratacoes_dates" in src
    assert "contratacoes_modalidades" in src
    assert "run_sliced_remaining_ingestion" in src

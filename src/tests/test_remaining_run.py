import inspect

from etl.ingestion.page_runner import run_page_batch_ingestion
from etl.ingestion.remaining_run import run_remaining_ingestion


def test_remaining_ingestion_defaults_to_sequential_pages() -> None:
    remaining = inspect.signature(run_remaining_ingestion).parameters["parallel_pages"]
    runner = inspect.signature(run_page_batch_ingestion).parameters["parallel_pages"]
    assert remaining.default == 1
    assert runner.default == 1


def test_remaining_ingestion_forwards_parallel_pages() -> None:
    remaining_src = inspect.getsource(run_remaining_ingestion)
    assert "parallel_pages=parallel_pages" in remaining_src

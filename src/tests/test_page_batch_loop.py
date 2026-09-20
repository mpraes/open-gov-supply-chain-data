import json
from pathlib import Path

import pytest

from etl.ingestion.page_loop import run_page_batch_loop
from observability.logging_json import get_json_logger


def _info_events(tmp_path: Path, logger_name: str) -> list[dict[str, object]]:
    path = tmp_path / f"{logger_name}_info.log"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


class FakePageStore:
    def __init__(
        self,
        start_page: int,
        pages: dict[int, tuple[list[dict[str, object]], int]],
    ) -> None:
        self.last = start_page
        self._pages = pages
        self.fetched: list[int] = []
        self.ingested: list[list[dict[str, object]]] = []
        self.saved: list[int] = []

    def load(self) -> int:
        return self.last

    def fetch(self, pagina: int) -> tuple[list[dict[str, object]], int]:
        self.fetched.append(pagina)
        return self._pages[pagina]

    def ingest(self, rows: list[dict[str, object]]) -> int:
        self.ingested.append(rows)
        return len(rows)

    def save(self, pagina: int) -> None:
        self.last = pagina
        self.saved.append(pagina)


def test_run_page_batch_loop_upserts_each_page_and_saves_cursor(tmp_path: Path) -> None:
    store = FakePageStore(
        0,
        {
            1: ([{"cod": 1}], 2),
            2: ([{"cod": 2}], 2),
        },
    )
    total = run_page_batch_loop(
        load_cursor=store.load,
        fetch_page=store.fetch,
        ingest_rows=store.ingest,
        save_cursor=store.save,
        log=get_json_logger("page_batch_loop", log_dir=tmp_path),
        job_name="material_item",
    )
    assert total == 2
    assert store.fetched == [1, 2]
    assert store.saved == [1, 2]
    assert store.ingested == [[{"cod": 1}], [{"cod": 2}]]
    events = _info_events(tmp_path, "page_batch_loop")
    assert all("duration_ms" in row for row in events)
    assert [row["message"] for row in events][-1] == "page_batches_done"


def test_run_page_batch_loop_resumes_after_last_saved_page(tmp_path: Path) -> None:
    store = FakePageStore(1, {2: ([{"cod": 2}], 2)})
    total = run_page_batch_loop(
        load_cursor=store.load,
        fetch_page=store.fetch,
        ingest_rows=store.ingest,
        save_cursor=store.save,
        log=get_json_logger("page_batch_resume", log_dir=tmp_path),
        job_name="material_item",
    )
    assert total == 1
    assert store.fetched == [2]
    assert store.saved == [2]


def test_run_page_batch_loop_does_not_advance_when_ingest_fails(tmp_path: Path) -> None:
    store = FakePageStore(0, {1: ([{"cod": 1}], 1)})

    def boom(rows: list[dict[str, object]]) -> int:
        store.ingested.append(rows)
        raise RuntimeError("network is unreachable")

    with pytest.raises(RuntimeError, match="network is unreachable"):
        run_page_batch_loop(
            load_cursor=store.load,
            fetch_page=store.fetch,
            ingest_rows=boom,
            save_cursor=store.save,
            log=get_json_logger("page_batch_fail", log_dir=tmp_path),
            job_name="material_item",
        )
    assert store.saved == []
    assert store.last == 0


def test_run_page_batch_loop_prefetches_later_pages_before_ingest(tmp_path: Path) -> None:
    from threading import Event, Lock

    fetched_at_ingest: list[list[int]] = []
    started: set[int] = set()
    both_started = Event()
    lock = Lock()
    store = FakePageStore(
        0,
        {
            1: ([{"cod": 1}], 3),
            2: ([{"cod": 2}], 3),
            3: ([{"cod": 3}], 3),
        },
    )

    def fetch(pagina: int) -> tuple[list[dict[str, object]], int]:
        with lock:
            store.fetched.append(pagina)
            started.add(pagina)
            if 2 in started and 3 in started:
                both_started.set()
        if pagina in (2, 3):
            assert both_started.wait(timeout=1)
        return store._pages[pagina]

    def ingest(rows: list[dict[str, object]]) -> int:
        with lock:
            fetched_at_ingest.append(list(store.fetched))
        return store.ingest(rows)

    total = run_page_batch_loop(
        load_cursor=store.load,
        fetch_page=fetch,
        ingest_rows=ingest,
        save_cursor=store.save,
        log=get_json_logger("page_batch_prefetch", log_dir=tmp_path),
        job_name="material_item",
        parallel_pages=2,
    )
    assert total == 3
    assert store.ingested == [[{"cod": 1}], [{"cod": 2}], [{"cod": 3}]]
    assert store.saved == [1, 2, 3]
    assert 2 in fetched_at_ingest[1] and 3 in fetched_at_ingest[1]


def test_run_page_batch_loop_does_not_fetch_past_total_pages(tmp_path: Path) -> None:
    store = FakePageStore(
        0,
        {
            1: ([{"cod": 1}], 2),
            2: ([{"cod": 2}], 2),
        },
    )
    total = run_page_batch_loop(
        load_cursor=store.load,
        fetch_page=store.fetch,
        ingest_rows=store.ingest,
        save_cursor=store.save,
        log=get_json_logger("page_batch_no_overfetch", log_dir=tmp_path),
        job_name="material_item",
        parallel_pages=4,
    )
    assert total == 2
    assert store.fetched == [1, 2]
    assert store.saved == [1, 2]

from logging import getLogger

import pytest

from etl.ingestion.page_loop import run_page_batch_loop


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


def test_run_page_batch_loop_upserts_each_page_and_saves_cursor() -> None:
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
        log=getLogger("page_batch_loop"),
        job_name="material_item",
    )
    assert total == 2
    assert store.fetched == [1, 2]
    assert store.saved == [1, 2]
    assert store.ingested == [[{"cod": 1}], [{"cod": 2}]]


def test_run_page_batch_loop_resumes_after_last_saved_page() -> None:
    store = FakePageStore(1, {2: ([{"cod": 2}], 2)})
    total = run_page_batch_loop(
        load_cursor=store.load,
        fetch_page=store.fetch,
        ingest_rows=store.ingest,
        save_cursor=store.save,
        log=getLogger("page_batch_resume"),
        job_name="material_item",
    )
    assert total == 1
    assert store.fetched == [2]
    assert store.saved == [2]


def test_run_page_batch_loop_does_not_advance_when_ingest_fails() -> None:
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
            log=getLogger("page_batch_fail"),
            job_name="material_item",
        )
    assert store.saved == []
    assert store.last == 0

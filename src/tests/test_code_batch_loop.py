from logging import getLogger

import pytest

from etl.ingestion.precos.batch_loop import run_code_batch_loop


class FakeCursorStore:
    def __init__(self, start: int, batches: list[list[int]]) -> None:
        self.last = start
        self._batches = list(batches)
        self.saved: list[int] = []
        self.ingested: list[list[int]] = []

    def load(self) -> int:
        return self.last

    def next_codes(self, last_code: int, batch_size: int) -> list[int]:
        if not self._batches:
            return []
        batch = self._batches.pop(0)
        assert last_code == self.last
        assert batch_size == 2
        return batch

    def save(self, last_code: int) -> None:
        self.last = last_code
        self.saved.append(last_code)

    def ingest(self, codes: list[int]) -> int:
        self.ingested.append(codes)
        return len(codes)


def test_run_code_batch_loop_upserts_each_small_batch_and_resumes() -> None:
    store = FakeCursorStore(0, [[10, 20], [30]])
    total = run_code_batch_loop(
        load_cursor=store.load,
        next_codes=store.next_codes,
        save_cursor=store.save,
        ingest_codes=store.ingest,
        batch_size=2,
        log=getLogger("preco_batch_loop"),
        job_name="preco_material",
    )
    assert total == 3
    assert store.ingested == [[10, 20], [30]]
    assert store.saved == [20, 30]
    assert store.last == 30


def test_run_code_batch_loop_does_not_advance_cursor_when_ingest_fails() -> None:
    store = FakeCursorStore(0, [[10, 20]])

    def boom(codes: list[int]) -> int:
        store.ingested.append(codes)
        raise RuntimeError("network is unreachable")

    with pytest.raises(RuntimeError, match="network is unreachable"):
        run_code_batch_loop(
            load_cursor=store.load,
            next_codes=store.next_codes,
            save_cursor=store.save,
            ingest_codes=boom,
            batch_size=2,
            log=getLogger("preco_batch_loop_fail"),
            job_name="preco_material",
        )
    assert store.saved == []
    assert store.last == 0

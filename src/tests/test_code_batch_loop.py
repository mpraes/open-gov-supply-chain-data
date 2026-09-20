import json
from pathlib import Path

import pytest

from etl.ingestion.precos.batch_loop import run_code_batch_loop
from observability.logging_json import get_json_logger


def _info_events(tmp_path: Path, logger_name: str) -> list[dict[str, object]]:
    path = tmp_path / f"{logger_name}_info.log"
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]


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


def test_run_code_batch_loop_upserts_each_small_batch_and_resumes(
    tmp_path: Path,
) -> None:
    store = FakeCursorStore(0, [[10, 20], [30]])
    total = run_code_batch_loop(
        load_cursor=store.load,
        next_codes=store.next_codes,
        save_cursor=store.save,
        ingest_codes=store.ingest,
        batch_size=2,
        log=get_json_logger("preco_batch_loop", log_dir=tmp_path),
        job_name="preco_material",
    )
    assert total == 3
    assert store.ingested == [[10, 20], [30]]
    assert store.saved == [20, 30]
    assert store.last == 30
    events = _info_events(tmp_path, "preco_batch_loop")
    batch_ok = [row for row in events if row["message"] == "preco_batch_ok"]
    done = [row for row in events if row["message"] == "preco_batches_done"]
    assert len(batch_ok) == 2
    assert all(isinstance(row["duration_ms"], int) for row in batch_ok + done)
    assert done[0]["rows"] == 3


def test_run_code_batch_loop_does_not_advance_cursor_when_ingest_fails(
    tmp_path: Path,
) -> None:
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
            log=get_json_logger("preco_batch_loop_fail", log_dir=tmp_path),
            job_name="preco_material",
        )
    assert store.saved == []
    assert store.last == 0

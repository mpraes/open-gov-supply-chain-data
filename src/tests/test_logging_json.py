import json
import logging
import re
from pathlib import Path

from observability.logging_json import get_json_logger, log_error, log_info, log_warning

ISO_TIMESTAMP = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})$"
)


def _read_json_lines(path: Path) -> list[dict[str, object]]:
    if not path.exists():
        return []
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line
    ]


def test_get_json_logger_writes_each_level_to_its_own_file(tmp_path: Path) -> None:
    log = get_json_logger("etl_file_split", log_dir=tmp_path)
    log_info(log, "info_event", row=1)
    log_warning(log, "warn_event", row=2)
    log_error(log, "error_event", row=3)

    info_rows = _read_json_lines(tmp_path / "etl_file_split_info.log")
    warn_rows = _read_json_lines(tmp_path / "etl_file_split_warning.log")
    error_rows = _read_json_lines(tmp_path / "etl_file_split_error.log")

    assert [row["message"] for row in info_rows] == ["info_event"]
    assert [row["message"] for row in warn_rows] == ["warn_event"]
    assert [row["message"] for row in error_rows] == ["error_event"]
    assert info_rows[0]["row"] == 1
    assert warn_rows[0]["row"] == 2
    assert error_rows[0]["row"] == 3


def test_log_lines_include_iso_timestamp(tmp_path: Path) -> None:
    log = get_json_logger("etl_timestamp", log_dir=tmp_path)
    log_info(log, "timed_event")
    info_rows = _read_json_lines(tmp_path / "etl_timestamp_info.log")
    assert len(info_rows) == 1
    assert isinstance(info_rows[0]["timestamp"], str)
    assert ISO_TIMESTAMP.match(info_rows[0]["timestamp"])


def test_get_json_logger_is_idempotent(tmp_path: Path) -> None:
    first = get_json_logger("etl_idempotent", log_dir=tmp_path)
    second = get_json_logger("etl_idempotent", log_dir=tmp_path)
    assert first is second
    assert len(first.handlers) == 4


def test_get_json_logger_keeps_stdout_handler(tmp_path: Path) -> None:
    log = get_json_logger("etl_stdout", log_dir=tmp_path)
    stream_logs = [
        stream
        for stream in log.handlers
        if isinstance(stream, logging.StreamHandler)
        and not isinstance(stream, logging.FileHandler)
    ]
    assert len(stream_logs) == 1


def test_get_json_logger_keeps_stdout_when_log_file_not_writable(
    tmp_path: Path,
) -> None:
    blocked = tmp_path / "etl_unwritable_info.log"
    blocked.write_text("", encoding="utf-8")
    blocked.chmod(0o444)
    try:
        log = get_json_logger("etl_unwritable", log_dir=tmp_path)
        log_info(log, "survived_unwritable_file")
    finally:
        blocked.chmod(0o644)
    stream_logs = [
        stream
        for stream in log.handlers
        if isinstance(stream, logging.StreamHandler)
        and not isinstance(stream, logging.FileHandler)
    ]
    assert len(stream_logs) == 1
    assert not blocked.read_text(encoding="utf-8")

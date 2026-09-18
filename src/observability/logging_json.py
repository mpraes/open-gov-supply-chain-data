import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

DEFAULT_LOG_DIR = Path(__file__).resolve().parent / "logs"


class JsonFormatter(logging.Formatter):
    """Format log records as one JSON object per line."""

    def format(self, record: logging.LogRecord) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created, tz=timezone.utc).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        extra_fields = getattr(record, "extra_fields", None)
        if isinstance(extra_fields, dict):
            payload.update(extra_fields)
        return json.dumps(payload, ensure_ascii=False)


class ExactLevelFilter(logging.Filter):
    """Allow only records with an exact levelno."""

    def __init__(self, level: int) -> None:
        super().__init__()
        self._level = level

    def filter(self, record: logging.LogRecord) -> bool:
        return record.levelno == self._level


def get_json_logger(
    name: str = "open_gov",
    level: int = logging.INFO,
    log_dir: Path | None = None,
) -> logging.Logger:
    """Return a JSON logger writing to stdout and per-level files.

    Example:
        log = get_json_logger("material_group")
        log_info(log, "api_fetch_ok", status_code=200)
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    target_dir = log_dir if log_dir is not None else DEFAULT_LOG_DIR
    target_dir.mkdir(parents=True, exist_ok=True)
    formatter = JsonFormatter()
    logger.addHandler(_build_stdout_handler(formatter))
    for level_name, level_no in (("info", logging.INFO), ("warning", logging.WARNING), ("error", logging.ERROR)):
        logger.addHandler(
            _build_level_file_handler(target_dir, name, level_name, level_no, formatter)
        )
    logger.setLevel(level)
    logger.propagate = False
    return logger


def _build_stdout_handler(formatter: logging.Formatter) -> logging.Handler:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    return handler


def _build_level_file_handler(
    log_dir: Path,
    logger_name: str,
    level_name: str,
    level_no: int,
    formatter: logging.Formatter,
) -> logging.Handler:
    path = log_dir / f"{logger_name}_{level_name}.log"
    handler = logging.FileHandler(path, encoding="utf-8")
    handler.setLevel(level_no)
    handler.addFilter(ExactLevelFilter(level_no))
    handler.setFormatter(formatter)
    return handler


def log_info(logger: logging.Logger, message: str, **fields: object) -> None:
    """Log an INFO event with structured fields."""
    logger.info(message, extra={"extra_fields": fields})


def log_warning(logger: logging.Logger, message: str, **fields: object) -> None:
    """Log a WARNING event with structured fields."""
    logger.warning(message, extra={"extra_fields": fields})


def log_error(logger: logging.Logger, message: str, **fields: object) -> None:
    """Log an ERROR event with structured fields."""
    logger.error(message, extra={"extra_fields": fields})

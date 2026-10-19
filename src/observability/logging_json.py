"""Logger JSON em stdout e em arquivos separados por nível."""

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LOG_DIR = Path(__file__).resolve().parent / "logs"


class JsonFormatter(logging.Formatter):
    """Formata registros de log como um objeto JSON por linha."""

    def format(self, record: logging.LogRecord) -> str:
        """Serializa timestamp, level, message, logger e extra_fields em uma linha JSON."""
        payload: dict[str, object] = {
            "timestamp": datetime.fromtimestamp(
                record.created, tz=timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        extra_fields = getattr(record, "extra_fields", None)
        if isinstance(extra_fields, dict):
            payload.update(extra_fields)
        return json.dumps(payload, ensure_ascii=False)


class ExactLevelFilter(logging.Filter):
    """Permite apenas registros com o levelno exato."""

    def __init__(self, level: int) -> None:
        """Guarda o levelno que o filtro aceita."""
        super().__init__()
        self._level = level

    def filter(self, record: logging.LogRecord) -> bool:
        """Aceita o registro somente quando levelno é igual ao nível guardado."""
        return record.levelno == self._level


def get_json_logger(
    name: str = "open_gov",
    level: int = logging.INFO,
    log_dir: Path | None = None,
) -> logging.Logger:
    """Retorna um logger JSON que escreve no stdout e em arquivos por nível.

    Exemplo:
        log = get_json_logger("material_group")
        log_info(log, "api_fetch_ok", status_code=200)
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger
    target_dir = log_dir if log_dir is not None else DEFAULT_LOG_DIR
    formatter = JsonFormatter()
    logger.addHandler(_build_stdout_log(formatter))
    _add_writable_file_logs(logger, target_dir, name, formatter)
    logger.setLevel(level)
    logger.propagate = False
    return logger


def _add_writable_file_logs(
    logger: logging.Logger,
    target_dir: Path,
    name: str,
    formatter: logging.Formatter,
) -> None:
    """Cria o diretório e anexa os arquivos info, warning e error quando a escrita é possível."""
    try:
        target_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        return
    for level_name, level_no in (
        ("info", logging.INFO),
        ("warning", logging.WARNING),
        ("error", logging.ERROR),
    ):
        file_log = _try_level_file_log(
            target_dir, name, level_name, level_no, formatter
        )
        if file_log is not None:
            logger.addHandler(file_log)


def _build_stdout_log(formatter: logging.Formatter) -> logging.Handler:
    """Monta o handler de stdout com o formatter JSON."""
    stdout_log = logging.StreamHandler(sys.stdout)
    stdout_log.setFormatter(formatter)
    return stdout_log


def _try_level_file_log(
    log_dir: Path,
    logger_name: str,
    level_name: str,
    level_no: int,
    formatter: logging.Formatter,
) -> logging.Handler | None:
    """Abre o arquivo do nível filtrado em levelno, ou devolve None se não puder criá-lo."""
    path = log_dir / f"{logger_name}_{level_name}.log"
    try:
        file_log = logging.FileHandler(path, encoding="utf-8")
    except OSError:
        return None
    file_log.setLevel(level_no)
    file_log.addFilter(ExactLevelFilter(level_no))
    file_log.setFormatter(formatter)
    return file_log


def log_info(logger: logging.Logger, message: str, **fields: object) -> None:
    """Registra um evento INFO com campos estruturados."""
    logger.info(message, extra={"extra_fields": fields})


def log_warning(logger: logging.Logger, message: str, **fields: object) -> None:
    """Registra um evento WARNING com campos estruturados."""
    logger.warning(message, extra={"extra_fields": fields})


def log_error(logger: logging.Logger, message: str, **fields: object) -> None:
    """Registra um evento ERROR com campos estruturados."""
    logger.error(message, extra={"extra_fields": fields})

from logging import getLogger, getLevelName, Logger, Formatter, INFO, StreamHandler, DEBUG
from pathlib import Path
from typing import Optional


def setup_logger(name: str, level: Optional[str] = None) -> Logger:
    logger = getLogger(name)
    formatter = prepare_formatter()
    logger.addHandler(prepare_console_handler(formatter))
    set_level(logger, level)
    logger.info(f'Logging is set up for "{name}"')
    return logger


def prepare_formatter() -> Formatter:
    return Formatter(
        '{asctime} | {levelname:^9} | [{filename}:{lineno}] {message}',
        datefmt='%Y-%m-%d %H:%M:%S',
        style='{',
    )


def prepare_console_handler(formatter: Formatter) -> StreamHandler:
    handler = StreamHandler()
    handler.setFormatter(formatter)
    handler.setLevel(INFO)
    return handler


def prepare_log_path(service_name: str) -> Path:
    log_dir = Path(__file__).parent / 'logs'
    log_dir.mkdir(parents=True, exist_ok=True)
    return (log_dir / f'{service_name}.log').absolute()


def set_level(logger: Logger, level: str) -> None:
    logger.setLevel(DEBUG)  # Must be set to the lowest level of the handlers.
    logger.setLevel(getLevelName(level or 'INFO'))

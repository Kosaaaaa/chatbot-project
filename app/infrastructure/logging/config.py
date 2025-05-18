import inspect
import logging
import sys
from typing import Final, Literal, final, override

from loguru import logger


@final
class InterceptHandler(logging.Handler):
    def __init__(self, level: int | str = 0, log_cast: dict[str, int] | None = None) -> None:
        super().__init__(level)
        self._log_mapper: dict[int, str] = {
            logging.DEBUG: "DEBUG",
            logging.INFO: "INFO",
            logging.WARNING: "WARNING",
            logging.ERROR: "ERROR",
            logging.CRITICAL: "CRITICAL",
        }
        self._log_cast = log_cast

    @override
    def emit(self, record: logging.LogRecord) -> None:  # noqa: PLR6301
        try:
            level = logger.level(record.levelname).name
            if self._log_cast is not None and record.name in self._log_cast:
                level = self._log_mapper[self._log_cast[record.name]]
        except ValueError:
            level = self._log_cast.get(record.name, record.levelno) if self._log_cast is not None else record.levelno

        frame, depth = inspect.currentframe(), 0
        while frame and (depth == 0 or frame.f_code.co_filename == logging.__file__):
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class LogConfig:
    def __init__(
        self,
        *,
        environment: Literal["local", "dev", "staging", "production"],
    ) -> None:
        self.environment: Final[Literal["local", "dev", "staging", "production"]] = environment

    @staticmethod
    def setup_local_environment() -> None:
        _ = logger.add(sys.stderr, level=logging.DEBUG, backtrace=True, diagnose=True, enqueue=True, colorize=True)

    @staticmethod
    def setup_production_environment() -> None:
        _ = logger.add(
            "logs/application.log",
            rotation="500 MB",
            compression="zip",
            level="INFO",
            backtrace=True,
            diagnose=True,
        )

    def configure(self) -> None:
        if self.environment == "local":
            self.setup_local_environment()
        else:
            self.setup_production_environment()


def setup_intercept_handlers():
    logger.remove()
    for handler in logging.root.handlers[:]:
        logging.root.removeHandler(handler)

    log_cast = {
        "sqlalchemy.engine.Engine": logging.DEBUG,
    }
    logging.basicConfig(handlers=[InterceptHandler(log_cast=log_cast)])

    loggers = (
        "uvicorn",
        "uvicorn.access",
        "uvicorn.error",
        "fastapi",
        "asyncio",
        "starlette",
        "sqlalchemy.engine.Engine",
    )

    for logger_name in loggers:
        logging_logger = logging.getLogger(logger_name)
        logging_logger.handlers = []
        logging_logger.propagate = True


def setup_logging(
    *,
    environment: Literal["local", "dev", "staging", "production"],
) -> None:
    setup_intercept_handlers()

    config = LogConfig(
        environment=environment,
    )
    config.configure()

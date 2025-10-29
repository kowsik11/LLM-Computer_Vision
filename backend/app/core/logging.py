import logging
import sys

import structlog


def configure_logging(level: int = logging.INFO) -> None:
    """Configure structured logging for the application."""

    timestamper = structlog.processors.TimeStamper(fmt="iso")
    processors = [
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_log_level,
        timestamper,
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ]

    structlog.configure(
        processors=processors,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=level,
    )


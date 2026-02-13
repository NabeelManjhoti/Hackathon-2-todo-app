"""Structured logging utilities."""

import json
import logging

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
)
logger = logging.getLogger(__name__)


class StructuredLogger:
    """Structured JSON logger for consistent log formatting."""

    @staticmethod
    def log(level: str, message: str, **kwargs: object) -> None:
        """Log a structured JSON message.

        Args:
            level: Log level (INFO, ERROR, etc.)
            message: Log message
            **kwargs: Additional fields to include in log
        """
        log_data = {
            "level": level,
            "message": message,
            **kwargs,
        }
        logger.log(getattr(logging, level), json.dumps(log_data))


# Global structured logger instance
structured_logger = StructuredLogger()

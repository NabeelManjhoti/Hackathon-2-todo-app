"""Retry decorator with exponential backoff for OpenAI API calls."""

import asyncio
import logging
from functools import wraps
from typing import Any, Callable, TypeVar

from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

logger = logging.getLogger(__name__)

# Type variable for generic function return type
T = TypeVar('T')


def retry_with_backoff(
    max_attempts: int = 3,
    min_wait: int = 2,
    max_wait: int = 10,
) -> Callable:
    """Decorator to retry async functions with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        min_wait: Minimum wait time in seconds (default: 2)
        max_wait: Maximum wait time in seconds (default: 10)

    Returns:
        Decorated function with retry logic

    Example:
        @retry_with_backoff(max_attempts=3)
        async def call_openai_api():
            # API call here
            pass
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        reraise=True,
    )


def sync_retry_with_backoff(
    max_attempts: int = 3,
    min_wait: int = 2,
    max_wait: int = 10,
) -> Callable:
    """Decorator to retry synchronous functions with exponential backoff.

    Args:
        max_attempts: Maximum number of retry attempts (default: 3)
        min_wait: Minimum wait time in seconds (default: 2)
        max_wait: Maximum wait time in seconds (default: 10)

    Returns:
        Decorated function with retry logic
    """
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=min_wait, max=max_wait),
        retry=retry_if_exception_type((ConnectionError, TimeoutError)),
        reraise=True,
    )

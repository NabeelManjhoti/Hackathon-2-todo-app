"""Timeout wrapper for OpenAI API calls."""

import asyncio
from typing import Any, Callable, TypeVar

from fastapi import HTTPException

T = TypeVar('T')


async def with_timeout(
    coro: Callable[..., Any],
    timeout_seconds: float = 30.0,
    error_message: str = "Operation timed out"
) -> Any:
    """Execute an async function with a timeout.

    Args:
        coro: Coroutine to execute
        timeout_seconds: Timeout in seconds (default: 30.0)
        error_message: Error message if timeout occurs

    Returns:
        Result of the coroutine

    Raises:
        HTTPException: 504 Gateway Timeout if operation exceeds timeout
    """
    try:
        result = await asyncio.wait_for(coro, timeout=timeout_seconds)
        return result
    except asyncio.TimeoutError:
        raise HTTPException(
            status_code=504,
            detail=f"{error_message} (exceeded {timeout_seconds}s timeout)"
        )


class TimeoutWrapper:
    """Context manager for timeout operations."""

    def __init__(self, timeout_seconds: float = 30.0):
        """Initialize timeout wrapper.

        Args:
            timeout_seconds: Timeout in seconds
        """
        self.timeout_seconds = timeout_seconds

    async def __aenter__(self):
        """Enter async context."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Exit async context."""
        return False

    async def execute(self, coro: Callable[..., Any]) -> Any:
        """Execute coroutine with timeout.

        Args:
            coro: Coroutine to execute

        Returns:
            Result of the coroutine

        Raises:
            HTTPException: 504 if timeout occurs
        """
        return await with_timeout(coro, self.timeout_seconds)

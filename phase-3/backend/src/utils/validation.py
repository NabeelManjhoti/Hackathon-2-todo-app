"""Input validation and sanitization for natural language input."""

import re
from typing import Optional

from fastapi import HTTPException


MAX_MESSAGE_LENGTH = 2000
MIN_MESSAGE_LENGTH = 1


def sanitize_message(message: str) -> str:
    """Sanitize user message input.

    Args:
        message: Raw user message

    Returns:
        Sanitized message

    Raises:
        HTTPException: 400 if message is invalid
    """
    # Strip whitespace
    message = message.strip()

    # Validate length
    if len(message) < MIN_MESSAGE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty"
        )

    if len(message) > MAX_MESSAGE_LENGTH:
        raise HTTPException(
            status_code=400,
            detail=f"Message too long (max {MAX_MESSAGE_LENGTH} characters)"
        )

    # Remove null bytes and other control characters (except newlines and tabs)
    message = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', message)

    # Normalize whitespace (collapse multiple spaces/newlines)
    message = re.sub(r'\s+', ' ', message)

    return message


def validate_conversation_id(conversation_id: Optional[str]) -> Optional[str]:
    """Validate conversation ID format.

    Args:
        conversation_id: Optional conversation ID string

    Returns:
        Validated conversation ID or None

    Raises:
        HTTPException: 400 if conversation_id format is invalid
    """
    if conversation_id is None:
        return None

    # UUID format validation (basic check)
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )

    if not uuid_pattern.match(conversation_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid conversation ID format (must be UUID)"
        )

    return conversation_id


def validate_user_id(user_id: str) -> str:
    """Validate user ID format.

    Args:
        user_id: User ID string

    Returns:
        Validated user ID

    Raises:
        HTTPException: 400 if user_id format is invalid
    """
    # UUID format validation
    uuid_pattern = re.compile(
        r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        re.IGNORECASE
    )

    if not uuid_pattern.match(user_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid user ID format (must be UUID)"
        )

    return user_id

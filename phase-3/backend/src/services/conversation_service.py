"""Conversation service for managing chat history and context."""

from typing import List
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.models.conversation import Conversation
from src.models.message import Message


async def load_conversation_history(
    session: AsyncSession,
    conversation_id: UUID,
    limit: int = 20
) -> List[Message]:
    """Load recent messages from database for agent context.

    Args:
        session: Database session
        conversation_id: Conversation ID
        limit: Maximum number of messages to load (default: 20)

    Returns:
        List of messages ordered by timestamp (oldest first)
    """
    # Query messages ordered by timestamp descending, then reverse
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp.desc())
        .limit(limit)
    )
    result = await session.execute(statement)
    messages = result.scalars().all()

    # Reverse to get oldest first (chronological order for agent context)
    return list(reversed(messages))


def format_messages_for_agent(messages: List[Message]) -> List[dict]:
    """Convert database messages to OpenAI API format.

    Args:
        messages: List of Message objects from database

    Returns:
        List of message dictionaries in OpenAI format
    """
    formatted_messages = []

    for msg in messages:
        formatted_msg = {
            "role": msg.role,
            "content": msg.content,
        }

        # Include tool_calls if present (for assistant messages)
        if msg.tool_calls:
            formatted_msg["tool_calls"] = msg.tool_calls

        formatted_messages.append(formatted_msg)

    return formatted_messages


async def get_or_create_conversation(
    session: AsyncSession,
    user_id: UUID,
    conversation_id: UUID | None = None
) -> Conversation:
    """Get existing conversation or create a new one.

    Args:
        session: Database session
        user_id: User ID
        conversation_id: Optional conversation ID to retrieve

    Returns:
        Conversation object

    Raises:
        ValueError: If conversation_id provided but not found or doesn't belong to user
    """
    if conversation_id:
        # Retrieve existing conversation
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await session.execute(statement)
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found or access denied")

        return conversation
    else:
        # Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        return conversation

"""Conversation service for managing chat history and context."""

from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from sqlalchemy import func, delete as sql_delete
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


async def list_user_conversations(
    session: AsyncSession,
    user_id: UUID,
    limit: int = 50,
    offset: int = 0
) -> Dict[str, any]:
    """List all conversations for a user with pagination.

    Args:
        session: Database session
        user_id: User ID
        limit: Maximum number of conversations to return
        offset: Number of conversations to skip

    Returns:
        Dictionary with conversations list and total count
    """
    # Get total count
    count_statement = (
        select(func.count(Conversation.id))
        .where(Conversation.user_id == user_id)
    )
    count_result = await session.execute(count_statement)
    total = count_result.scalar_one()

    # Get conversations with message count and last message
    statement = (
        select(Conversation)
        .where(Conversation.user_id == user_id)
        .order_by(Conversation.updated_at.desc())
        .limit(limit)
        .offset(offset)
    )
    result = await session.execute(statement)
    conversations = result.scalars().all()

    # Format conversations with additional data
    conversations_data = []
    for conv in conversations:
        # Get message count
        msg_count_stmt = (
            select(func.count(Message.id))
            .where(Message.conversation_id == conv.id)
        )
        msg_count_result = await session.execute(msg_count_stmt)
        message_count = msg_count_result.scalar_one()

        # Get last message
        last_msg_stmt = (
            select(Message)
            .where(Message.conversation_id == conv.id)
            .order_by(Message.timestamp.desc())
            .limit(1)
        )
        last_msg_result = await session.execute(last_msg_stmt)
        last_message = last_msg_result.scalar_one_or_none()

        conversations_data.append({
            "id": str(conv.id),
            "created_at": conv.created_at.isoformat(),
            "updated_at": conv.updated_at.isoformat(),
            "message_count": message_count,
            "last_message": last_message.content[:100] if last_message else None
        })

    return {
        "conversations": conversations_data,
        "total": total
    }


async def get_conversation_with_messages(
    session: AsyncSession,
    user_id: UUID,
    conversation_id: UUID
) -> Optional[Dict[str, any]]:
    """Get a conversation with all its messages.

    Args:
        session: Database session
        user_id: User ID
        conversation_id: Conversation ID

    Returns:
        Dictionary with conversation details and messages, or None if not found
    """
    # Get conversation with user isolation
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    result = await session.execute(statement)
    conversation = result.scalar_one_or_none()

    if not conversation:
        return None

    # Get all messages for this conversation
    messages_stmt = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp.asc())
    )
    messages_result = await session.execute(messages_stmt)
    messages = messages_result.scalars().all()

    # Format messages
    messages_data = [
        {
            "id": str(msg.id),
            "role": msg.role,
            "content": msg.content,
            "tool_calls": msg.tool_calls,
            "timestamp": msg.timestamp.isoformat()
        }
        for msg in messages
    ]

    return {
        "id": str(conversation.id),
        "created_at": conversation.created_at.isoformat(),
        "updated_at": conversation.updated_at.isoformat(),
        "messages": messages_data
    }


async def delete_user_conversation(
    session: AsyncSession,
    user_id: UUID,
    conversation_id: UUID
) -> bool:
    """Delete a conversation and all its messages.

    Args:
        session: Database session
        user_id: User ID
        conversation_id: Conversation ID

    Returns:
        True if deleted, False if not found or access denied
    """
    # Verify conversation exists and belongs to user
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id
    )
    result = await session.execute(statement)
    conversation = result.scalar_one_or_none()

    if not conversation:
        return False

    # Delete conversation (messages will cascade delete due to relationship)
    await session.delete(conversation)
    await session.commit()

    return True

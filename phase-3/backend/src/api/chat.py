"""Chat endpoint for AI chatbot."""

from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.auth import get_current_user
from src.dependencies.database import get_session
from src.logger import structured_logger
from src.models.conversation import Conversation
from src.models.message import Message
from src.models.user import User
from src.services.agent_runner import run_agent
from src.services.conversation_service import (
    format_messages_for_agent,
    get_or_create_conversation,
    load_conversation_history,
)
from src.utils.validation import sanitize_message, validate_conversation_id


router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    message: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""

    conversation_id: str
    response: str
    tool_calls: Optional[list] = None


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Send message to AI chatbot",
    description="Send a natural language message to the AI chatbot for task management",
)
async def chat(
    user_id: str,
    chat_request: ChatRequest,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ChatResponse:
    """Send message to AI chatbot and get response.

    Args:
        user_id: User ID from path parameter
        chat_request: Chat request with message and optional conversation_id
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        Chat response with conversation_id, response text, and tool_calls

    Raises:
        HTTPException: 400 for invalid input, 403 for user_id mismatch, 404 for conversation not found
    """
    try:
        # Validate user_id matches authenticated user
        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch - cannot access other user's chat"
            )

        # Sanitize and validate input
        user_message = sanitize_message(chat_request.message)
        conversation_id_str = validate_conversation_id(chat_request.conversation_id)

        # Get or create conversation
        conversation_id_uuid = UUID(conversation_id_str) if conversation_id_str else None
        conversation = await get_or_create_conversation(
            session=session,
            user_id=current_user.id,
            conversation_id=conversation_id_uuid
        )

        structured_logger.log(
            "INFO",
            "Chat request received",
            user_id=user_id,
            conversation_id=str(conversation.id),
            message_length=len(user_message)
        )

        # Store user message
        user_msg = Message(
            conversation_id=conversation.id,
            role="user",
            content=user_message,
            timestamp=datetime.utcnow(),
        )
        session.add(user_msg)
        await session.commit()

        # Load conversation history (last 20 messages)
        history_messages = await load_conversation_history(
            session=session,
            conversation_id=conversation.id,
            limit=20
        )

        # Format messages for agent (exclude the just-added user message)
        formatted_history = format_messages_for_agent(history_messages[:-1])

        # Run agent with conversation history and new message
        agent_result = await run_agent(
            session=session,
            user_id=user_id,
            conversation_history=formatted_history,
            user_message=user_message
        )

        # Store assistant response
        assistant_msg = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=agent_result["response"],
            tool_calls=agent_result.get("tool_calls"),
            timestamp=datetime.utcnow(),
        )
        session.add(assistant_msg)
        await session.commit()

        structured_logger.log(
            "INFO",
            "Chat response generated",
            user_id=user_id,
            conversation_id=str(conversation.id),
            tool_calls_count=len(agent_result.get("tool_calls", []))
        )

        # Return formatted response
        return ChatResponse(
            conversation_id=str(conversation.id),
            response=agent_result["response"],
            tool_calls=agent_result.get("tool_calls")
        )

    except HTTPException:
        # Re-raise HTTP exceptions
        raise
    except ValueError as e:
        # Handle validation errors
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        # Log and return generic error
        structured_logger.log(
            "ERROR",
            "Chat endpoint error",
            user_id=user_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error processing chat request"
        )

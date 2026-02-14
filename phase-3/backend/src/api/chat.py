"""Chat endpoint for AI chatbot."""

from datetime import datetime
from typing import Annotated, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address
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


# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

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


class ConversationListItem(BaseModel):
    """Conversation list item model."""

    id: str
    created_at: str
    updated_at: str
    message_count: int
    last_message: Optional[str] = None


class ConversationListResponse(BaseModel):
    """Response model for conversation list."""

    conversations: list[ConversationListItem]
    total: int


class MessageItem(BaseModel):
    """Message item model."""

    id: str
    role: str
    content: str
    tool_calls: Optional[dict] = None
    timestamp: str


class ConversationDetailResponse(BaseModel):
    """Response model for conversation detail."""

    id: str
    created_at: str
    updated_at: str
    messages: list[MessageItem]


@router.post(
    "/{user_id}/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
    summary="Send message to AI chatbot",
    description="Send a natural language message to the AI chatbot for task management",
)
@limiter.limit("60/minute")
async def chat(
    request: Request,
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
            error=str(e),
            error_type=type(e).__name__
        )

        # Check for database-related errors
        error_msg = str(e).lower()
        if any(keyword in error_msg for keyword in ["database", "connection", "timeout", "operational"]):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Database service is temporarily unavailable. Please try again in a moment."
            )

        # Generic error fallback
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error processing chat request"
        )


@router.get(
    "/{user_id}/conversations",
    response_model=ConversationListResponse,
    status_code=status.HTTP_200_OK,
    summary="List all conversations",
    description="Get a list of all conversations for the authenticated user",
)
async def list_conversations(
    user_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
    limit: int = 50,
    offset: int = 0,
) -> ConversationListResponse:
    """List all conversations for the user.

    Args:
        user_id: User ID from path parameter
        current_user: Authenticated user from JWT token
        session: Database session
        limit: Maximum number of conversations to return (default 50)
        offset: Number of conversations to skip (default 0)

    Returns:
        List of conversations with metadata

    Raises:
        HTTPException: 403 for user_id mismatch
    """
    try:
        # Validate user_id matches authenticated user
        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch - cannot access other user's conversations"
            )

        # Import here to avoid circular dependency
        from src.services.conversation_service import list_user_conversations

        # Get conversations
        conversations_data = await list_user_conversations(
            session=session,
            user_id=current_user.id,
            limit=limit,
            offset=offset
        )

        return ConversationListResponse(
            conversations=conversations_data["conversations"],
            total=conversations_data["total"]
        )

    except HTTPException:
        raise
    except Exception as e:
        structured_logger.log(
            "ERROR",
            "Failed to list conversations",
            user_id=user_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error listing conversations"
        )


@router.get(
    "/{user_id}/conversations/{conversation_id}",
    response_model=ConversationDetailResponse,
    status_code=status.HTTP_200_OK,
    summary="Get conversation details",
    description="Get a specific conversation with all messages",
)
async def get_conversation(
    user_id: str,
    conversation_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> ConversationDetailResponse:
    """Get conversation details with all messages.

    Args:
        user_id: User ID from path parameter
        conversation_id: Conversation ID from path parameter
        current_user: Authenticated user from JWT token
        session: Database session

    Returns:
        Conversation details with messages

    Raises:
        HTTPException: 403 for user_id mismatch, 404 for conversation not found
    """
    try:
        # Validate user_id matches authenticated user
        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch - cannot access other user's conversations"
            )

        # Validate conversation_id format
        conversation_id_str = validate_conversation_id(conversation_id)
        conversation_uuid = UUID(conversation_id_str)

        # Import here to avoid circular dependency
        from src.services.conversation_service import get_conversation_with_messages

        # Get conversation
        conversation_data = await get_conversation_with_messages(
            session=session,
            user_id=current_user.id,
            conversation_id=conversation_uuid
        )

        if not conversation_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or you don't have permission to access it"
            )

        return ConversationDetailResponse(**conversation_data)

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        structured_logger.log(
            "ERROR",
            "Failed to get conversation",
            user_id=user_id,
            conversation_id=conversation_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error retrieving conversation"
        )


@router.delete(
    "/{user_id}/conversations/{conversation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete conversation",
    description="Delete a conversation and all its messages",
)
async def delete_conversation(
    user_id: str,
    conversation_id: str,
    current_user: Annotated[User, Depends(get_current_user)],
    session: Annotated[AsyncSession, Depends(get_session)],
) -> None:
    """Delete a conversation and all its messages.

    Args:
        user_id: User ID from path parameter
        conversation_id: Conversation ID from path parameter
        current_user: Authenticated user from JWT token
        session: Database session

    Raises:
        HTTPException: 403 for user_id mismatch, 404 for conversation not found
    """
    try:
        # Validate user_id matches authenticated user
        if str(current_user.id) != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User ID mismatch - cannot access other user's conversations"
            )

        # Validate conversation_id format
        conversation_id_str = validate_conversation_id(conversation_id)
        conversation_uuid = UUID(conversation_id_str)

        # Import here to avoid circular dependency
        from src.services.conversation_service import delete_user_conversation

        # Delete conversation
        deleted = await delete_user_conversation(
            session=session,
            user_id=current_user.id,
            conversation_id=conversation_uuid
        )

        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found or you don't have permission to delete it"
            )

        structured_logger.log(
            "INFO",
            "Conversation deleted",
            user_id=user_id,
            conversation_id=conversation_id
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        structured_logger.log(
            "ERROR",
            "Failed to delete conversation",
            user_id=user_id,
            conversation_id=conversation_id,
            error=str(e)
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error deleting conversation"
        )

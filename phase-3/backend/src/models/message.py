"""Message database model for AI chatbot."""

from datetime import datetime
from typing import TYPE_CHECKING, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .conversation import Conversation


class Message(SQLModel, table=True):
    """Message entity representing individual messages in a conversation.

    Attributes:
        id: Unique message identifier (UUID)
        conversation_id: Parent conversation (UUID, foreign key to conversations)
        role: Message sender role - "user", "assistant", or "system"
        content: Message text content
        tool_calls: Optional JSON record of tool invocations
        timestamp: Timestamp when message was created
        metadata: Optional JSON metadata (tokens used, model version, etc.)
    """

    __tablename__ = "messages"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="Unique message identifier",
    )
    conversation_id: UUID = Field(
        foreign_key="conversations.id",
        nullable=False,
        index=True,
        description="Parent conversation",
    )
    role: str = Field(
        nullable=False,
        description="Message sender role: user, assistant, or system",
    )
    content: str = Field(
        nullable=False,
        max_length=10000,
        description="Message text content",
    )
    tool_calls: Optional[dict] = Field(
        default=None,
        nullable=True,
        sa_column_kwargs={"type_": "JSONB"},
        description="Optional record of tool invocations",
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="Timestamp when message was created",
    )
    metadata: Optional[dict] = Field(
        default=None,
        nullable=True,
        sa_column_kwargs={"type_": "JSONB"},
        description="Optional metadata (tokens used, model version)",
    )

    # Relationship
    conversation: "Conversation" = Relationship(back_populates="messages")

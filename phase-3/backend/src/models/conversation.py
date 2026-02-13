"""Conversation database model for AI chatbot."""

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .message import Message


class Conversation(SQLModel, table=True):
    """Conversation entity representing a chat session.

    Attributes:
        id: Unique conversation identifier (UUID)
        user_id: Owner of the conversation (UUID, foreign key to users)
        created_at: Timestamp when conversation was created
        updated_at: Timestamp when conversation was last updated
        metadata: Optional JSON metadata (title, summary, tags)
    """

    __tablename__ = "conversations"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="Unique conversation identifier",
    )
    user_id: UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True,
        description="User who owns this conversation",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="Timestamp when conversation was created",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when conversation was last updated",
    )
    metadata: Optional[dict] = Field(
        default=None,
        nullable=True,
        sa_column_kwargs={"type_": "JSONB"},
        description="Optional metadata (title, summary, tags)",
    )

    # Relationship
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )

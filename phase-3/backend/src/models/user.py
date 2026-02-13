"""User database model for authentication."""

from datetime import datetime
from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User entity for authentication and authorization.

    Attributes:
        id: Unique user identifier (UUID)
        email: User email address (unique, used for login)
        password_hash: Hashed password (never exposed in API responses)
        created_at: Timestamp when user account was created
        updated_at: Timestamp when user account was last updated
    """

    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="Unique user identifier",
    )
    email: str = Field(
        nullable=False,
        unique=True,
        index=True,
        description="User email address (unique, indexed for login lookups)",
    )
    password_hash: str = Field(
        nullable=False,
        description="Hashed password (bcrypt, never exposed in API)",
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when user account was created",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Timestamp when user account was last updated",
    )

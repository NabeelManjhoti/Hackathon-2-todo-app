"""User database model (placeholder for future authentication)."""

from uuid import UUID, uuid4

from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    """User entity (placeholder for future authentication integration).

    This is a minimal structure to establish foreign key relationship
    with Task entity. Full authentication will be implemented in a future spec.

    Attributes:
        id: Unique user identifier (UUID)
        email: User email address (unique)
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
        description="User email address",
    )

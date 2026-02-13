"""Authentication request/response schemas."""

from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field


class SignupRequest(BaseModel):
    """Request schema for user registration.

    Attributes:
        email: User email address (must be valid email format)
        password: User password (minimum 8 characters)
    """

    email: EmailStr = Field(
        ...,
        description="User email address (must be valid email format)",
    )
    password: str = Field(
        ...,
        min_length=8,
        description="User password (minimum 8 characters)",
    )


class SigninRequest(BaseModel):
    """Request schema for user authentication.

    Attributes:
        email: User email address
        password: User password
    """

    email: EmailStr = Field(
        ...,
        description="User email address",
    )
    password: str = Field(
        ...,
        description="User password",
    )


class UserResponse(BaseModel):
    """Response schema for user information (without sensitive data).

    Attributes:
        id: Unique user identifier
        email: User email address
        created_at: Timestamp when user account was created
    """

    id: UUID = Field(
        ...,
        description="Unique user identifier",
    )
    email: str = Field(
        ...,
        description="User email address",
    )
    created_at: datetime = Field(
        ...,
        description="Timestamp when user account was created",
    )

    class Config:
        """Pydantic configuration."""

        from_attributes = True


class AuthResponse(BaseModel):
    """Response schema for authentication endpoints.

    Attributes:
        access_token: JWT access token
        token_type: Token type (always "bearer")
        user: User information (without password)
    """

    access_token: str = Field(
        ...,
        description="JWT access token",
    )
    token_type: str = Field(
        default="bearer",
        description="Token type (always bearer)",
    )
    user: UserResponse = Field(
        ...,
        description="User information (without password)",
    )

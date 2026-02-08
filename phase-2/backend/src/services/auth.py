"""Authentication service with password hashing and JWT token management."""

from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

import jwt
from passlib.context import CryptContext

from src.config import settings

# Password hashing context using bcrypt
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hash a password using bcrypt.

    Args:
        password: Plain text password to hash

    Returns:
        Hashed password string
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Hashed password to compare against

    Returns:
        True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(user_id: UUID, email: str) -> str:
    """Create a JWT access token for a user.

    Args:
        user_id: User's unique identifier
        email: User's email address

    Returns:
        Encoded JWT token string
    """
    # Calculate expiration time
    expire = datetime.utcnow() + timedelta(minutes=settings.jwt_expiry_minutes)

    # Create token payload with standard claims
    payload = {
        "sub": str(user_id),  # Subject (user ID)
        "email": email,  # Custom claim for user email
        "exp": expire,  # Expiration time
        "iat": datetime.utcnow(),  # Issued at time
    }

    # Encode and return token
    token = jwt.encode(payload, settings.jwt_secret, algorithm=settings.jwt_algorithm)
    return token


def decode_access_token(token: str) -> Optional[dict]:
    """Decode and verify a JWT access token.

    Args:
        token: JWT token string to decode

    Returns:
        Decoded token payload if valid, None otherwise

    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.InvalidTokenError: If token is invalid or tampered
    """
    try:
        payload = jwt.decode(
            token, settings.jwt_secret, algorithms=[settings.jwt_algorithm]
        )
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        raise
    except jwt.InvalidTokenError:
        # Token is invalid (bad signature, malformed, etc.)
        raise

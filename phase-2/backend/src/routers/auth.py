"""Authentication API endpoints."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from src.dependencies.auth import get_current_user
from src.dependencies.database import get_session
from src.logger import structured_logger
from src.models.user import User
from src.schemas.auth import AuthResponse, SigninRequest, SignupRequest, UserResponse
from src.services.auth import create_access_token, hash_password, verify_password

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/signup", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    request: SignupRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthResponse:
    """Register a new user account.

    Creates a new user with email and password, returns user info and JWT token.

    Args:
        request: Signup request with email and password
        session: Database session

    Returns:
        AuthResponse with user info and JWT token

    Raises:
        HTTPException: 409 if email already registered
        HTTPException: 400 if validation fails
    """
    # Check if email already exists
    result = await session.execute(select(User).where(User.email == request.email))
    existing_user = result.scalar_one_or_none()

    if existing_user is not None:
        structured_logger.log(
            "WARNING",
            "Signup attempt with existing email",
            email=request.email,
        )
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    # Hash password
    password_hash = hash_password(request.password)

    # Create new user
    new_user = User(
        email=request.email,
        password_hash=password_hash,
    )

    session.add(new_user)
    await session.commit()
    await session.refresh(new_user)

    structured_logger.log(
        "INFO",
        "User registered successfully",
        user_id=str(new_user.id),
        email=new_user.email,
    )

    # Generate JWT token
    token = create_access_token(new_user.id, new_user.email)

    # Return user info and token
    return AuthResponse(
        user=UserResponse.model_validate(new_user),
        token=token,
    )


@router.post("/signin", response_model=AuthResponse)
async def signin(
    request: SigninRequest,
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AuthResponse:
    """Authenticate user and receive JWT token.

    Verifies email and password, returns user info and JWT token.

    Args:
        request: Signin request with email and password
        session: Database session

    Returns:
        AuthResponse with user info and JWT token

    Raises:
        HTTPException: 401 if credentials are invalid
    """
    # Look up user by email
    result = await session.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()

    # Verify user exists and password is correct
    if user is None or not verify_password(request.password, user.password_hash):
        structured_logger.log(
            "WARNING",
            "Failed login attempt",
            email=request.email,
        )
        # Generic error message to prevent user enumeration
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
        )

    structured_logger.log(
        "INFO",
        "User signed in successfully",
        user_id=str(user.id),
        email=user.email,
    )

    # Generate JWT token
    token = create_access_token(user.id, user.email)

    # Return user info and token
    return AuthResponse(
        user=UserResponse.model_validate(user),
        token=token,
    )


@router.post("/logout")
async def logout(
    current_user: Annotated[User, Depends(get_current_user)],
) -> dict:
    """Invalidate current session (client-side token removal).

    This endpoint confirms the user is authenticated and logs the logout event.
    Actual token invalidation happens on the client side by removing the token.

    Args:
        current_user: Authenticated user from JWT token

    Returns:
        Success message
    """
    structured_logger.log(
        "INFO",
        "User logged out",
        user_id=str(current_user.id),
        email=current_user.email,
    )

    return {"message": "Logged out successfully"}

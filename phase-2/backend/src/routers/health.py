"""Health check endpoint."""

from typing import Dict

from fastapi import APIRouter, Depends, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from src.dependencies.database import get_db

router = APIRouter(tags=["health"])


@router.get(
    "/health",
    status_code=status.HTTP_200_OK,
    summary="Health check",
    description="Check if the API is running and database is accessible",
)
async def health_check(db: AsyncSession = Depends(get_db)) -> Dict[str, str]:
    """Check API and database health.

    Args:
        db: Database session from dependency injection

    Returns:
        Dictionary with status and database connection state

    Raises:
        HTTPException: 503 if database is not accessible
    """
    try:
        # Test database connection
        await db.execute(text("SELECT 1"))
        return {
            "status": "healthy",
            "database": "connected",
        }
    except Exception:
        return {
            "status": "unhealthy",
            "database": "disconnected",
        }

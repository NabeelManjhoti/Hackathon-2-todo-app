"""Database engine and session configuration."""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlmodel import SQLModel

from src.config import settings

# Create async engine with connection pooling
engine: AsyncEngine = create_async_engine(
    settings.database_url,
    echo=False,  # Set to True for SQL query logging
    pool_size=5,
    max_overflow=10,
    pool_recycle=300,  # Recycle connections after 5 minutes
    pool_pre_ping=True,  # Verify connections before using
)


async def create_db_and_tables() -> None:
    """Create database tables on startup.

    This function creates all tables defined in SQLModel models.
    Should be called during application startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

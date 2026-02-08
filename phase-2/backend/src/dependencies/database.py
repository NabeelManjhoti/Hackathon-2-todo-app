"""Database session dependency for dependency injection."""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel.ext.asyncio.session import AsyncSession as SQLModelAsyncSession

from src.database import engine


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Provide database session for dependency injection.

    Yields:
        AsyncSession: Database session for the request

    Example:
        @app.get("/items")
        async def get_items(db: AsyncSession = Depends(get_db)):
            result = await db.execute(select(Item))
            return result.scalars().all()
    """
    async with SQLModelAsyncSession(engine) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

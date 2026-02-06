from typing import AsyncGenerator, cast
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings

# Create Async Engine
# echo=True allows seeing generated SQL queries in logs (useful for debugging)
engine = create_async_engine(
    cast(str, settings.DATABASE_URL),
    echo=settings.DEBUG,
    future=True,
    pool_pre_ping=True,  # Check connection validity before using it
    pool_size=10,        # Maximum number of connections in the pool
    max_overflow=20      # Maximum number of connections to create beyond pool_size
)

# Create Session Factory
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,  # Prevent attributes from being expired after commit
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency function to get a database session.
    Ensures the session is closed after the request is finished.
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

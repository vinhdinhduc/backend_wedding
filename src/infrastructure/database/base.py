"""Database configuration helpers for the refactored project structure."""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.main.config import settings

engine: AsyncEngine | None = None


def init_database() -> None:
    global engine
    if engine is None:
        engine = create_async_engine(settings.DATABASE_URL, echo=False)


async def shutdown_database() -> None:
    global engine
    if engine is not None:
        await engine.dispose()
        engine = None

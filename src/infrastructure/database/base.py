"""Database configuration helpers for the refactored project structure."""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from src.main.config import settings


FALLBACK_DATABASE_URL = "sqlite+aiosqlite:///./tienmung.db"


class Base(DeclarativeBase):
    """Shared SQLAlchemy base for infrastructure models."""


engine: AsyncEngine | None = None
database_url: str | None = None


def init_database(url: str | None = None) -> None:
    global engine, database_url
    if engine is None:
        chosen_url = url or settings.DATABASE_URL
        try:
            engine = create_async_engine(
                chosen_url,
                echo=not settings.is_production,
                pool_pre_ping=True,
            )
            database_url = chosen_url
        except ModuleNotFoundError:
            if chosen_url == FALLBACK_DATABASE_URL:
                raise
            engine = create_async_engine(
                FALLBACK_DATABASE_URL,
                echo=not settings.is_production,
                pool_pre_ping=True,
            )
            database_url = FALLBACK_DATABASE_URL


async def shutdown_database() -> None:
    global engine, database_url
    if engine is not None:
        await engine.dispose()
        engine = None
        database_url = None

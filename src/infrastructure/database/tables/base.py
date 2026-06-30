"""SQLALchemy async, tất cả ORM đều phải import từ đây"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from src.main.config import settings


NAMING_CONVENTION: dict[str, str] = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

class Base(DeclarativeBase):
    """Base class cho tất cả các ORM"""
    metadata = MetaData(naming_convention=NAMING_CONVENTION)



engine = create_async_engine(settings.DATABASE_URL, 
                              echo = not settings.is_production, pool_pre_ping= True, pool_recycle = 3600, max_overflow = 10, pool_size = 20, future = True)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit= False, class_=AsyncSession
                                       , expire_on_commit=False, autoflush=False, autocommit=False)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Fast dependency injection 
    Dùng async def my_route
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()





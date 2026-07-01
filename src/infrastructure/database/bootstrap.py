from __future__ import annotations

from collections.abc import Sequence
from dataclasses import dataclass
from uuid import UUID

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.infrastructure.database import base as db_base
from src.infrastructure.database.models.ho_gia_dinh import HoGiaDinh

_pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass(frozen=True)
class SampleHousehold:
    id: UUID
    email: str
    password: str


SAMPLE_HOUSEHOLDS: Sequence[SampleHousehold] = (
    SampleHousehold(UUID("11111111-1111-1111-1111-111111111101"), "hohung@example.com", "TienMung@123"),
    SampleHousehold(UUID("11111111-1111-1111-1111-111111111102"), "holannga@example.com", "TienMung@123"),
    SampleHousehold(UUID("11111111-1111-1111-1111-111111111103"), "minhkhoi@example.com", "TienMung@123"),
    SampleHousehold(UUID("11111111-1111-1111-1111-111111111104"), "thuha@example.com", "TienMung@123"),
)


async def bootstrap_database() -> None:
    """Create the auth table and seed a small set of sample households."""
    db_base.init_database()
    try:
        await _bootstrap_with_current_engine()
    except Exception:
        if db_base.database_url == db_base.FALLBACK_DATABASE_URL:
            raise

        await db_base.shutdown_database()
        db_base.init_database(db_base.FALLBACK_DATABASE_URL)
        await _bootstrap_with_current_engine()


async def _bootstrap_with_current_engine() -> None:
    if db_base.engine is None:
        raise RuntimeError("Database engine was not initialized.")

    async with db_base.engine.begin() as connection:
        await connection.run_sync(db_base.Base.metadata.create_all)

    session_factory = async_sessionmaker(db_base.engine, expire_on_commit=False, class_=AsyncSession)
    async with session_factory() as session:
        await seed_sample_households(session)
        await session.commit()


async def seed_sample_households(session: AsyncSession) -> None:
    """Insert sample households only when the table is empty."""
    existing = await session.scalar(select(HoGiaDinh.id).limit(1))
    if existing is not None:
        return

    session.add_all(
        [
            HoGiaDinh(
                id=str(sample.id),
                email=sample.email,
                mat_khau_hash=_pwd_context.hash(sample.password),
            )
            for sample in SAMPLE_HOUSEHOLDS
        ]
    )

from __future__ import annotations

from datetime import datetime
from uuid import UUID

from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.database.base import Base


class HoGiaDinh(Base):
    """SQLAlchemy model for the `ho_gia_dinh` table."""

    __tablename__ = "ho_gia_dinh"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True, nullable=False, index=True)
    mat_khau_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    ngay_tao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
    ngay_cap_nhat: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )

    def as_uuid(self) -> UUID:
        return UUID(self.id)

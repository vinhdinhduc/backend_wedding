from __future__ import annotations

from datetime import datetime, timezone
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.i_ho_gia_dinh_repo import IHoGiaDinhRepo
from src.domain.entities.ho_gia_dinh import HoGiaDinhEntity
from src.domain.exceptions import NotFoundError
from src.infrastructure.database.models.ho_gia_dinh import HoGiaDinhModel



class HoGiaDinhRepo(IHoGiaDinhRepo):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    async def get_by_email(self, email: str) -> HoGiaDinhEntity | None:
        """Tìm hộ theo email"""
        stmt = select(HoGiaDinhModel).where(HoGiaDinhModel.email == email.strip().lower())
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None
    async def get_password_hash(self, id: UUID) -> str | None:
        """Lấy hash mật khẩu của hộ"""
        stmt = select(HoGiaDinhModel.password_hash).where(HoGiaDinhModel.id == str(id))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
    
    async def get_by_id(self, id: UUID) -> HoGiaDinhEntity | None:
        """Tìm hộ theo id"""
        stmt = select(HoGiaDinhModel).where(HoGiaDinhModel.id == str(id))
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()
        return model.to_entity() if model else None
    
    async def update_password(self, id: UUID, new_hash: str) -> None:
        """Cập  nhật mật khẩu hash dùng cho reset và đổi mật khẩu"""
        stmt = update(HoGiaDinhModel).where(HoGiaDinhModel.id == str(id)).values(
            mat_khau_hash = new_hash, ngay_cap_nhat = datetime.now(timezone.utc)

        )
        await self.session.execute(stmt)
    
    async def update(self, id: UUID, ho_gia_dinh_entity: HoGiaDinhEntity) -> None:
        """Cập nhật các trường tùy ý"""
        #Loại bỏ các trường không cho phép update trực tiếp
        _PROTECTED_FIELDS = {"id", "mat_khau_hash", "ngay_tao"}
        safe_kwargs = {k: v for k, v in kwargs.items() if k not in _PROTECTED_FIELDS}

        stmt = update(HoGiaDinhModel).where(HoGiaDinhModel.id == str(id)).values(**safe_kwargs).returning(HoGiaDinhModel)
        result = await self.session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            raise NotFoundError(f"Không tìm thấy hộ gia đình với id = {id}", code="HO_GIA_DINH_NOT_FOUND")
        return model.to_entity()
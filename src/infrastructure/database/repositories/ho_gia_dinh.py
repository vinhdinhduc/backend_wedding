from __future__ import annotations

from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.interfaces.i_ho_gia_dinh_repo import IHoGiaDinhRepo
from src.domain.entities.ho_gia_dinh import HoGiaDinhEntity
from src.infrastructure.database.models.ho_gia_dinh import HoGiaDinh


class SQLHoGiaDinhRepository(IHoGiaDinhRepo):
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    def _to_entity(self, row: HoGiaDinh) -> HoGiaDinhEntity:
        return HoGiaDinhEntity(
            id=UUID(row.id),
            email=row.email,
            ten_ho=None,
            ngay_tao=row.ngay_tao,
            ngay_cap_nhat=row.ngay_cap_nhat,
        )

    async def get_by_email(self, email: str) -> HoGiaDinhEntity | None:
        stmt = select(HoGiaDinh).where(HoGiaDinh.email == email)
        result = await self._session.execute(stmt)
        row = result.scalar_one_or_none()
        return None if row is None else self._to_entity(row)

    async def get_by_id(self, id: UUID) -> HoGiaDinhEntity | None:
        row = await self._session.get(HoGiaDinh, str(id))
        return None if row is None else self._to_entity(row)

    async def get_password_hash(self, id: UUID) -> str | None:
        stmt = select(HoGiaDinh.mat_khau_hash).where(HoGiaDinh.id == str(id))
        result = await self._session.execute(stmt)
        return result.scalar_one_or_none()

    async def update_password(self, id: UUID, new_hash: str) -> None:
        stmt = (
            update(HoGiaDinh)
            .where(HoGiaDinh.id == str(id))
            .values(mat_khau_hash=new_hash, ngay_cap_nhat=datetime.now(UTC))
        )
        await self._session.execute(stmt)

    async def update(self, id: UUID, **kwargs: object) -> HoGiaDinhEntity:
        values: dict[str, object] = {}
        email = kwargs.get("email")
        if isinstance(email, str) and email.strip():
            values["email"] = email.strip().lower()

        if values:
            stmt = (
                update(HoGiaDinh)
                .where(HoGiaDinh.id == str(id))
                .values(**values, ngay_cap_nhat=datetime.now(UTC))
            )
            await self._session.execute(stmt)

        entity = await self.get_by_id(id)
        if entity is None:
            from src.domain.exceptions import NotFoundError

            raise NotFoundError("Không tìm thấy hộ gia đình.", code="HO_GIA_DINH_NOT_FOUND")
        return entity

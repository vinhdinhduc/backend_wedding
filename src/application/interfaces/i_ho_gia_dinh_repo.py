from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID

from src.domain.entities.ho_gia_dinh import HoGiaDinhEntity


class IHoGiaDinhRepo(ABC): 
    @abstractmethod
    async def get_by_email(self, email: str) -> HoGiaDinhEntity | None:

        """Tìm hộ gia đình theo email."""
    
    @abstractmethod
    async def get_by_id(self, id: UUID) -> HoGiaDinhEntity | None:
        """Tìm hộ gia đình theo id."""


    @abstractmethod
    async def get_password_hash(self, id: UUID) -> str | None:
        """
        Lấy mat_khau_hash của hộ — chỉ dùng nội bộ auth flow.
        Không expose hash ra domain entity (security).

        Returns:
            bcrypt hash string, hoặc None nếu không tìm thấy.
        """
        ...

    @abstractmethod
    async def update_password(self, id: UUID, new_hash: str) -> None:
        """Cập nhật mat_khau_hash sau khi đổi/reset mật khẩu."""
        ...

    @abstractmethod
    async def update(self, id: UUID, **kwargs: object) -> HoGiaDinhEntity:
        """
        Cập nhật các trường của HoGiaDinh (ten_ho, email...).

        Args:
            id: UUID của hộ cần cập nhật.
            **kwargs: Các trường và giá trị mới.

        Returns:
            HoGiaDinhEntity đã cập nhật.

        Raises:
            NotFoundError: Nếu không tìm thấy hộ với id này.
        """
        ...


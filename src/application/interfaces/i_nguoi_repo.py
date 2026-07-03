"""
Interface (ABC) cho Nguoi repository.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from enum import Enum
from uuid import UUID

from src.domain.entities.nguoi import NguoiEntity


class SortEnum(str, Enum):
    """Các tiêu chí sắp xếp danh sách người."""
    TEN_A_Z = "TEN_A_Z"                   # Sắp theo tên không dấu A→Z
    GIAO_DICH_GAN_NHAT = "GIAO_DICH_GAN_NHAT"  # Sắp theo ngày tạo LanMung/LanDiMung gần nhất
    NO_NHIEU_NHAT = "NO_NHIEU_NHAT"       # Sắp theo tổng tiền chưa mừng lại (DESC)


class INguoiRepo(ABC):
    """Abstract repository cho Nguoi."""

    @abstractmethod
    async def create(
        self,
        ho_gia_dinh_id: UUID,
        ten_hien_thi: str,
        ten_khong_dau: str,
        ten_bi_danh: str | None,
        ghi_chu: str | None,
    ) -> NguoiEntity:
        """
        Tạo mới một người trong danh bạ hộ.

        Args:
            ho_gia_dinh_id: UUID hộ sở hữu.
            ten_hien_thi: Tên hiển thị đầy đủ.
            ten_khong_dau: Tên đã normalize (sinh tự động ở app layer).
            ten_bi_danh: Bí danh / tên gọi khác (nullable).
            ghi_chu: Ghi chú thêm (nullable).

        Returns:
            NguoiEntity vừa tạo.
        """
        ...

    @abstractmethod
    async def get_by_id(self, id: UUID, ho_gia_dinh_id: UUID) -> NguoiEntity | None:
        """
        Tìm người theo id, BẮT BUỘC filter thêm ho_gia_dinh_id (C-05).

        Returns:
            NguoiEntity nếu tìm thấy và thuộc hộ, None nếu không.
        """
        ...

    @abstractmethod
    async def search(
        self,
        ho_gia_dinh_id: UUID,
        keyword: str,
        keyword_khong_dau: str,
    ) -> list[NguoiEntity]:
        """
        Tìm kiếm người theo tên (có dấu hoặc không dấu).

        Tìm theo OR:
            ten_hien_thi ILIKE %keyword%
            OR ten_khong_dau ILIKE %keyword_khong_dau%

        Args:
            ho_gia_dinh_id: Chỉ tìm trong hộ này.
            keyword: Từ khóa gốc (có thể có dấu).
            keyword_khong_dau: Từ khóa đã normalize không dấu.

        Returns:
            Danh sách NguoiEntity phù hợp, sắp theo ten_khong_dau.
        """
        ...

    @abstractmethod
    async def list_all(
        self,
        ho_gia_dinh_id: UUID,
        sort_by: SortEnum,
    ) -> list[NguoiEntity]:
        """
        Lấy toàn bộ danh sách người của hộ với tiêu chí sắp xếp.

        NO_NHIEU_NHAT: subquery SUM(lan_mung.so_tien) WHERE trang_thai CHUA_MUNG_LAI,
        sắp giảm dần. Người không có LanMung nào xếp cuối.
        """
        ...

    @abstractmethod
    async def update(
        self,
        id: UUID,
        ho_gia_dinh_id: UUID,
        **kwargs: object,
    ) -> NguoiEntity:
        """
        Cập nhật thông tin người.

        Args:
            id: UUID người cần update.
            ho_gia_dinh_id: BẮT BUỘC — đảm bảo chỉ update người thuộc hộ (C-05).
            **kwargs: Các trường cần cập nhật.

        Raises:
            NotFoundError: Nếu không tìm thấy hoặc sai hộ.
        """
        ...

    @abstractmethod
    async def check_has_history(self, id: UUID, ho_gia_dinh_id: UUID) -> bool:
        """
        Kiểm tra người có lịch sử LanMung hoặc LanDiMung không (C-04).
        Dùng trước khi xóa — hiện tại hệ thống không cho xóa nếu có lịch sử.

        Returns:
            True nếu còn lịch sử liên quan.
        """
        ...

    @abstractmethod
    async def count_by_ho(self, ho_gia_dinh_id: UUID) -> int:
        """Đếm tổng số người trong hộ."""
        ...

    @abstractmethod
    async def find_duplicate_name(
        self,
        ho_gia_dinh_id: UUID,
        ten_khong_dau: str,
        exclude_id: UUID | None = None,
    ) -> NguoiEntity | None:
        """
        Kiểm tra trùng tên trong hộ (so sánh ten_khong_dau).
        Dùng để warn người dùng (không block).

        Args:
            exclude_id: Bỏ qua bản ghi này khi check (dùng khi update).
        """
        ...
from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.application.interfaces.i_nguoi_repo import INguoiRepo
from src.application.interfaces.i_lich_su_repo import ILichSuRepo
from src.application.utils.audit_helper import compute_diff
from src.application.utils.text_normalize import normalize_vietnamese
from src.domain.entities.ho_gia_dinh import HoGiaDinhEntity
from src.domain.entities.nguoi import NguoiEntity
from src.domain.exceptions import NotFoundError, ValidationError


@dataclass
class SuaNguoiInput:
    ten_hien_thi: str
    ten_bi_danh: str | None
    ghi_chu: str | None

class SuaNguoiInteractor:
    def __init__(self, repo: INguoiRepo, lich_su_repo: ILichSuRepo) -> None:
        self.repo = repo
        self.lich_su_repo = lich_su_repo
    
    async def execute(
        self,
        input_dto: SuaNguoiInput,
        nguoi_id: UUID,
        current_user: HoGiaDinhEntity,
    ) -> NguoiEntity:
        existing = await self.repo.get_by_id(id = nguoi_id, ho_gia_dinh_id=current_user.id)
        if existing is None:
            raise NotFoundError("Không tìm thấy người hoặc bạn không có quyền truy cập.", code = "NGUOI_NOT_FOUND")
        #Chuẩn bị dict các field cần update
        update_kwargs: dict[str, object] = {}
        old_values: dict[str, object] = {}
        new_values: dict[str, object] = {}

        if input_dto.ten_hien_thi is not None:
            ten=input_dto.ten_hien_thi.strip()
            if not ten:
                raise ValidationError("Tên hiển thị không được để trống.", code="TEN_HIEN_THI_EMPTY")
            if len(ten) > 200:
                raise ValidationError("Tên hiển thị không được vượt quá 200 ký tự.", code="TEN_HIEN_THI_TOO_LONG")
            

            if ten != existing.ten_hien_thi:
                update_kwargs["ten_hien_thi"] = ten
                update_kwargs["ten_khong_dau"] = normalize_vietnamese(ten)
                old_values["ten_hien_thi"] = existing.ten_hien_thi
                new_values["ten_hien_thi"] = ten
        if input_dto.ten_bi_danh is not None:
            chu=input_dto.ten_bi_danh.strip() or None
            if chu != existing.ten_bi_danh:
                update_kwargs["ten_bi_danh"] = chu
                old_values["ten_bi_danh"] = existing.ten_bi_danh
                new_values["ten_bi_danh"] = chu
        #No change return original
        if not update_kwargs:
            return existing
        #ghi audit log
        log_entries = compute_diff(
            bang="nguoi",
            ban_ghi_id=nguoi_id,
            ho_gia_dinh_id=current_user.id,
            old_values=old_values,
            new_values=new_values,
        )
        if log_entries:
            await self.lich_su_repo.log_bulk(log_entries)
        

        updated = await self.repo.update(
            id=nguoi_id,
            ho_gia_dinh_id=current_user.id,
            **update_kwargs
        )

        return updated


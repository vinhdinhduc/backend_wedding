from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.application.interfaces.i_nguoi_repo import INguoiRepo
from src.application.utils.text_normalize import normalize_vietnamese
from src.domain.entities.ho_gia_dinh import HoGiaDinhEntity
from src.domain.entities.nguoi import NguoiEntity
from src.domain.exceptions import ValidationError


@dataclass
class ThemNguoiInput:
    ten_hien_thi: str
    ten_bi_danh: str | None
    ghi_chu: str | None



@dataclass  
class ThemNguoiOutput:
    entity: NguoiEntity
    warning_trung_ten: bool = False
    warning_nguoi_trung: NguoiEntity | None = None

class ThemNGuoiInteractor:
    def __init__(self, repo: INguoiRepo) -> None:
        self.repo = repo
    
    async def execute(
            self, input_dto: ThemNguoiInput,
            current_user: HoGiaDinhEntity
    ) -> ThemNguoiOutput:
        ten = input_dto.ten_hien_thi.strip()

        if not ten:
            raise ValidationError("Tên hiển thị không được để trống.", code="TEN_HIEN_THI_EMPTY")
        
        if len(ten) > 200:
            raise ValidationError("Tên hiển thị không được vượt quá 200 ký tự.", code="TEN_HIEN_THI_TOO_LONG")
        ten_khong_dau = normalize_vietnamese(ten)

        #check kiểm tra trùng tên
        duplicate = await self.repo.find_duplicate_name(ho_gia_dinh_id=current_user.id, ten_khong_dau=ten_khong_dau)

        #create record
        entity = await self.repo.create(
            ho_gia_dinh_id=current_user.id,
            ten_hien_thi=ten,
            ten_khong_dau=ten_khong_dau
            ten_bi_danh=input_dto.ten_bi_danh.strip() if input_dto.ten_bi_danh else None,
            ghi_chu=input_dto.ghi_chu.strip() if input_dto.ghi_chu else None
        )

        return ThemNguoiOutput(
            entity=entity,
            warning_trung_ten= duplicate is not None,
            warning_nguoi_trung=duplicate
        )
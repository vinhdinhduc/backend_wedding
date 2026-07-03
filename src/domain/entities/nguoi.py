from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class NguoiEntity:
    id: UUID
    ho_gia_dinh_id: UUID
    ten_hien_thi: str
    ten_khong_dau: str          # auto-generated tại application layer — không nhận từ client
    ten_bi_danh: str | None
    ghi_chu: str | None
    ngay_tao: datetime
    ngay_cap_nhat: datetime
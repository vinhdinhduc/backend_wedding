from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class HoGiaDinhEntity:
    id: UUID
    email: str
    ten_ho: str | None
    ngay_tao: datetime
    ngay_cap_nhat: datetime
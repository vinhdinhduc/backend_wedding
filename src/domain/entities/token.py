from __future__ import annotations

from dataclasses import dataclass, field
from uuid import UUID



@dataclass
class TokenEntity:
    access_token: str
    token_type: str = "Bearer"
    ho_gia_dinh_id: UUID | None = None
    email: str | None = None
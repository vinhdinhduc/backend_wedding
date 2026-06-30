"""Seed 5 loại sự kiện mặc định.

Revision ID: 001_seed
Revises:
Create Date: 2026-05-25
"""
from __future__ import annotations

import uuid
from alembic import op
import sqlalchemy as sa

revision: str = "001_seed"
down_revision: str | None = None
branch_labels = None
depends_on = None

LOAI_SU_KIEN_DEFAULTS = [
    {"ma": "CUOI",         "ten_hien_thi": "Cưới",               "thu_tu": 1},
    {"ma": "TAN_GIA",      "ten_hien_thi": "Tân gia",            "thu_tu": 2},
    {"ma": "SINH_NHAT",    "ten_hien_thi": "Sinh nhật con/cháu", "thu_tu": 3},
    {"ma": "DAM_MA",       "ten_hien_thi": "Đám ma",             "thu_tu": 4},
    {"ma": "GIUP_LAM_NHA", "ten_hien_thi": "Giúp làm nhà",      "thu_tu": 5},
]


def upgrade() -> None:
    loai_su_kien_table = sa.table(
        "loai_su_kien",
        sa.column("id", sa.String(36)),
        sa.column("ma", sa.String(50)),
        sa.column("ten_hien_thi", sa.String(200)),
        sa.column("thu_tu", sa.SmallInteger()),
        sa.column("ho_gia_dinh_id", sa.String(36)),
    )
    op.bulk_insert(
        loai_su_kien_table,
        [
            {
                "id": str(uuid.uuid4()),
                "ma": item["ma"],
                "ten_hien_thi": item["ten_hien_thi"],
                "thu_tu": item["thu_tu"],
                "ho_gia_dinh_id": None,  # NULL = mặc định toàn hệ thống
            }
            for item in LOAI_SU_KIEN_DEFAULTS
        ],
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM loai_su_kien WHERE ho_gia_dinh_id IS NULL "
        "AND ma IN ('CUOI','TAN_GIA','SINH_NHAT','DAM_MA','GIUP_LAM_NHA')"
    )
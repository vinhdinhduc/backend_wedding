"""
Alembic migration environment — cấu hình cho async MySQL.
Import tất cả ORM models để Alembic phát hiện schema thay đổi (autogenerate).
"""
import asyncio
from logging.config import fileConfig

from alembic import context
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from src.main.config import settings
from src.infrastructure.database.base import Base

# ── Import tất cả models để Alembic nhận dạng metadata ────────────────
# Thêm import ở đây khi tạo model mới
from src.infrastructure.database.models import ( 
    ho_gia_dinh,
    nguoi,
    loai_su_kien,
    su_kien,
    lan_mung,
    lan_di_mung,
    trang_thai_mung_lai,
    lich_su_chinh_sua,
)

# ── Alembic config ─────────────────────────────────────────────────────
config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


# ── Offline mode (tạo SQL scripts mà không kết nối DB) ────────────────
def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        compare_server_default=True,
    )
    with context.begin_transaction():
        context.run_migrations()


# ── Online mode (async) ────────────────────────────────────────────────
def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
        compare_type=True,
        compare_server_default=True,
        # MySQL không hỗ trợ transactional DDL — tắt transaction wrapper
        transaction_per_migration=False,
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,  # dùng NullPool cho migration scripts
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


# ── Dispatch ───────────────────────────────────────────────────────────
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
from __future__ import annotations

from uuid import UUID

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from src.domain.entities.ho_gia_dinh import HoGiaDinhEntity
from src.domain.exceptions import BusinessRuleError, NotFoundError


oauth_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


async def get_current_user(
        token: str = Depends(oauth_scheme)
) -> HoGiaDinhEntity:
    """"
    FastAPI dependency function  decode jwt và trả về HoGiaDinh Entiy của người dùng hiện tại"""
    from fastapi import HTTPException, status
    from dependency_injector.wiring import inject, Provide
    from src.main.ioc.container import Container
    from src.infrastructure.adapters.token_service import TokenService
    from src.infrastructure.adapters.ho_gia_dinh_repo import HoGiaDinhRepo
    from src.infrastructure.database.base import AsyncSessionFactory

    _401 = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail = "Phiên đăng nhập không hợp lệ hoặc đã hết hạn.",
        headers={"WWW-Authenticate": "Bearer"},
    )
    #Lấy service từ container
    from src.main.app import app as _app
    container: Container = _app.state.container
    token_service = container.token_service()

    try:
        payload = token_service.decode_token(token)
    except (BusinessRuleError, Exception):
        raise _401
    user_id_str: str | None = payload.get("sub")   
    if not user_id_str:
        raise _401
    
    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise _401
    
    #Tạo session và query user
    async with AsyncSessionFactory() as session:
        repo = HoGiaDinhRepo(session)
        entity = await repo.get_by_id(user_id)

    if entity is None:
        raise _401
    return entity
from __future__ import annotations

from dataclasses import dataclass

from src.application.interfaces.i_ho_gia_dinh_repo import IHoGiaDinhRepo
from src.application.interfaces.i_token_service import ITokenService
from src.domain.entities.token import TokenEntity
from src.domain.exceptions import BusinessRuleError



@dataclass 
class LoginInput:
    """DTO đầu vào cho đăng nhập"""
    email: str
    password: str


class LoginIneractor:
    def __init__(self,
                 repo: IHoGiaDinhRepo,
                 token_service: ITokenService
                 ) -> None:
        self.repo = repo
        self.token_service = token_service

    async def excute(self, input_dto: LoginInput) -> TokenEntity:
        """Thực hiện đăng nhập"""
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        _INVALID_CREDENTIALS_MSG = "Email hoặc mật khẩu không đúng."


        entity = await self.repo.get_by_email(input_dto.email)
        if entity is None:
            raise BusinessRuleError(_INVALID_CREDENTIALS_MSG)

        password_hashed = await self.repo.get_password_hash(entity.id)
        if password_hashed is None or not pwd_context.verify(input_dto.password, password_hashed):
            raise BusinessRuleError(_INVALID_CREDENTIALS_MSG)

        access_token = self.token_service.create_access_token(
            data= {"sub": str(entity.id), "email": entity.email}
        )

        return TokenEntity(
            access_token=access_token,
            token_type="bearer",
            ho_gia_dinh_id=entity.id,
            email=entity.email
        )
        

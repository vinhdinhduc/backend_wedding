from __future__ import annotations

from dataclasses import dataclass

from src.application.interfaces.i_ho_gia_dinh_repo import IHoGiaDinhRepo
from src.application.interfaces.i_token_service import ITokenService
from src.application.validators import validate_password_strength
from src.domain.exceptions import BusinessRuleError


@dataclass
class ResetPasswordInput:
    """DTO đầu vào cho đặt lại mật khẩu """
    token: str
    new_password: str


class ResetPasswordInteractor:
    def __init__(self, 
                 repo: IHoGiaDinhRepo,
                 token_service: ITokenService
                 ) -> None:
        self.repo = repo
        self.token_service = token_service
    async def excute(self, input_dto: ResetPasswordInput) -> None:
        """Đặt lại mật khẩu """
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

        email = self.token_service.decode_reset_token(input_dto.token)
        
        #validate new password 
        validate_password_strength(input_dto.new_password)

        entity = await self.repo.get_by_email(email)
        if entity is None: 
            raise BusinessRuleError("Token không hợp lệ hoặc đã hết hạn.", code="INVALID_RESET_TOKEN")
        
        new_hash = pwd_context.hash(input_dto.new_password)
        await self.repo.update_password(entity.id, new_hash)
        

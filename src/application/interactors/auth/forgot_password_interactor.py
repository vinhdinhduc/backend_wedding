from __future__ import annotations

from dataclasses import dataclass

from src.application.interfaces.i_email_service import IEmailService
from src.application.interfaces.i_ho_gia_dinh_repo import IHoGiaDinhRepo
from src.application.interfaces.i_token_service import ITokenService
from src.application.validators import validate_email_format
from src.main.config import settings


@dataclass
class ForgotPasswordInput:
    """DTO đầu vào cho quên mật khẩu """
    email: str
    frontend_url: str = "https: //wedding.app"

class ForgotPasswordInteractor:
    def __init__(self, 
                 repo: IHoGiaDinhRepo,
                 token_service: ITokenService,
                 email_service: IEmailService
                 ) -> None:
        self.repo = repo
        self.token_service = token_service
        self.email_service = email_service

    async def excute(self, input_dto: ForgotPasswordInput) -> None:
        """Gửi email quên mật khẩu"""
        validate_email_format(input_dto.email)
        normalized_email = input_dto.email.lower()
        entity = await self.repo.get_by_email(normalized_email)
        if entity is None:
            return 
        
        reset_token = self.token_service.create_reset_token(
            email=normalized_email,

        )
        reset_link = (
            f"{input_dto.frontend_url}/reset-password?token={reset_token}"
        
        )
        await self.email_service.send_reset_password(
            to_email=normalized_email,
            reset_link=reset_link
        )
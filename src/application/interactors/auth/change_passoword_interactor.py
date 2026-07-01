from __future__ import annotations

from dataclasses import dataclass
from uuid import UUID

from src.application.interfaces.i_ho_gia_dinh_repo import IHoGiaDinhRepo
from src.application.validators import validate_password_strength
from src.domain.exceptions import BusinessRuleError, NotFoundError

@dataclass 
class ChangePasswordInput:
    """DTO đầu vào cho đổi mật khẩu"""
    ho_gia_dinh_id: UUID
    old_password: str
    new_password: str

class ChangePasswordInteractor:
    def __init__(self, repo: IHoGiaDinhRepo) -> None:
        self.repo = repo

    async def excute(self, input_dto: ChangePasswordInput, current_user_id: UUID) -> None:
        """Thực hiện đổi mật khẩu"""
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


        current_hash = await self.repo.get_password_hash(current_user_id)
        if current_hash is None:
            raise NotFoundError("Không tìm thấy tài khoản.", code="USER_NOT_FOUND")
        
        if not pwd_context.verify(input_dto.old_password, current_hash):
            raise BusinessRuleError("Mật khẩu hiện tại không chính xác.", code="INVALID_OLD_PASSWORD")
        
        #VALIDATE NEW PASSWORD
        validate_password_strength(input_dto.new_password)
        #Không cho đặt lại mật khẩu cũ
        if pwd_context.verify(input_dto.new_password, current_hash):
            raise BusinessRuleError("Mật khẩu mới không được trùng với mật khẩu hiện tại.", code="NEW_PASSWORD_SAME_AS_OLD")
        new_hash = pwd_context.hash(input_dto.new_password)
        await self.repo.update_password(current_user_id, new_hash)

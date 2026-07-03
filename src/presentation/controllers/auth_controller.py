from __future__ import annotations

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel, EmailStr, Field

from src.application.interactors.auth.change_password_interactor import (
    ChangePasswordInput,
    ChangePasswordInteractor,
)
from src.application.interactors.auth.forgot_password_interactor import (
    ForgotPasswordInput,
    ForgotPasswordInteractor,
)
from src.application.interactors.auth.login_interactor import (
    LoginInput,
    LoginInteractor,
)
from src.application.interactors.auth.reset_password_interactor import (
    ResetPasswordInput,
    ResetPasswordInteractor,
)
from src.domain.entities.ho_gia_dinh import HoGiaDinhEntity
from src.presentation.dependencies import get_current_use

router = APIRouter(
    prefix="/api/v1/auth", tags=["Auth"]

)

class LoginRequest(BaseModel):
    email: EmailStr
    password:str

class TokenReponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ForgotPasswordRequest(BaseModel):
    email: EmailStr
    frontend_base_url: str = Field(default="https://wedding.app", title="URL trang web frontend")


class ResetPasswordRequest(BaseModel):
    token: str = Field(min_length=1)
    new_password: str = Field(min_length=8)


class ChangePasswordRequest(BaseModel):
    current_password: str = Field(min_length=1)
    new_password: str = Field(min_length=8)


class MessageResponse(BaseModel):
    message: str



def _get_login_interactor() -> LoginInteractor:
    from src.main.app import app as _app
    c = _app.state.container
    session = c.db_session()
    return LoginInteractor(
        repo=c.ho_gia_dinh_repo(session=session),
        token_service=c.token_service(),

    )

def _get_forgot_password_interactor() -> ForgotPasswordInteractor:
    from src.main.app import app as _app
    c = _app.state.container
    session = c.db_session()
    return ResetPasswordInteractor(
        repo=c.ho_gia_dinh_repo(session=session),
        token_service=c.token_service(),
        email_service=c.email_service(),
    )

def _get_reset_password_interactor() -> ResetPasswordInteractor:
    from src.main.app import app as _app
    c = _app.state.container
    session = c.db_session()
    return ResetPasswordInteractor(
        repo=c.ho_gia_dinh_repo(session=session),
        token_service=c.token_service(),
    )

def _get_change_password_interactor() -> ChangePasswordInteractor:
    from src.main.app import app as _app
    c = _app.state.container
    session = c.db_session()
    return ChangePasswordInteractor(
        repo=c.ho_gia_dinh_repo(session=session),
    )

@router.post("/login", response_model=TokenReponse, sumary="Đăng nhập hệ thống", description="Đăng nhập bằng email và mật khẩu. Trả về JWT access token")
async def login(
    body: LoginRequest,
    interactor: LoginInteractor = Depends(_get_login_interactor)
) -> TokenReponse:
    result = await interactor.execute(LoginInput(email=body.email, password=body.password))
    return TokenReponse(
        access_token=result.access_token,
        token_type=result.token_type
    )

@router.post("/forgot-password", sumary="Quên mật khẩu", description="Gửi link đặt lại mật khẩu email luôn trả về 200 dù thành công hay thất bại để bảo nật", status_code=status.HTTP_200_OK)
async def forgot_password(
    body: ForgotPasswordRequest,
    interactor: ForgotPasswordInteractor = Depends(_get_forgot_password_interactor)
) -> MessageResponse:
    await interactor.execute(ForgotPasswordInput(email=body.email, frontend_base_url=body.frontend_base_url))
    return MessageResponse(message="Nếu email tồn tại trong hệ thống, chúng tôi sẽ gửi link mật khẩu. ")

@router.post("/reset-password", sumary="Khoi phuc mat khau", description="Gui email de khoi phuc mat khau", status_code=status.HTTP_200_OK)
async def reset_password(
    body: ResetPasswordRequest,
    interactor: ResetPasswordInteractor = Depends(_get_reset_password_interactor)
) -> MessageResponse:
    await interactor.execute(ResetPasswordInput(token=body.token, new_password=body.new_password))
    return MessageResponse(message="Mật khẩu đã được đặt lại thành công")



@router.post("/change-password", summary="Đổi mật khẩu", description="Đổi mật khau", response_model=MessageResponse)
async def change_password(
    body: ChangePasswordRequest,
    current_user_id: HoGiaDinhEntity = Depends(get_current_user),
) -> MessageResponse:
    await interactor.execute(ChangePasswordInput(current_password=body.current_password, new_password=body.new_password), current_user_id=current_user_id.id)
    return MessageResponse(message="Mật khẩu đã được thay đổi thành công.")
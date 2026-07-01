


from __future__ import annotations
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from src.application.interfaces.i_token_service import ITokenService
from src.domain.exceptions import BusinessRuleError


_RESET_TOKEN_TYPE = "reset"

class TokenService(ITokenService):

    """JWT token service dùng python-jose để tạo và xác thực JWT token."""

    def __init__(self, secret_key: str, algorithm: str, expire_minutes: int) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def create_access_token(self, data: dict) -> str:
        """Tạo JWT access token với payload cho trước """
        now = datetime.now(timezone.utc)
        payload = {
            **data,
            "iat": now,
            "exp": now + timedelta(minutes=self.expire_minutes),
        
        }
        return jwt.encode(payload, self._secret_key, algorithm=self.algorithm)
    def decode_token(self, token: str) -> dict:

        """Decode và verify access token"""

        try: 
            payload = jwt.decode(token, self._secret_key, algorithms=[self.algorithm])
            if payload.get("type") == _RESET_TOKEN_TYPE:
                raise BusinessRuleError("Token không hợp lệ ", code="INVALID_RESET_TOKEN")
            return payload
        except JWTError:
            raise BusinessRuleError("Token không hợp lệ", code="INVALID_TOKEN")
    
    def create_reset_token(self, email: str) -> str:
        """
        Tạo reset token expire sau 1 giờ.

        Payload:
            {
                "sub": "<email>",
                "type": "reset",
                "iat": <issued_at>,
                "exp": <now + 3600s>
            }
        """
        now = datetime.now(timezone.utc)
        payload = {
            "sub": email,
            "type": _RESET_TOKEN_TYPE,
            "iat": now,
            "exp": now + timedelta(seconds=3600),
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def decode_reset_token(self, token: str) -> str:
        """
        Decode reset token và trả về email.

        Raises:
            BusinessRuleError: Nếu token invalid, hết hạn, hoặc không phải type=reset.
        """
        try:
            payload = jwt.decode(
                token,
                self._secret_key,
                algorithms=[self._algorithm],
            )
        except JWTError as exc:
            raise BusinessRuleError(
                "Link đặt lại mật khẩu không hợp lệ hoặc đã hết hạn.",
                code="INVALID_RESET_TOKEN",
            ) from exc

        if payload.get("type") != _RESET_TOKEN_TYPE:
            raise BusinessRuleError(
                "Link đặt lại mật khẩu không hợp lệ.",
                code="INVALID_RESET_TOKEN_TYPE",
            )

        email = payload.get("sub")
        if not email:
            raise BusinessRuleError(
                "Token không chứa thông tin hợp lệ.",
                code="INVALID_RESET_TOKEN_PAYLOAD",
            )

        return email
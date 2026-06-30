"""
Interface cho token service — tạo và decode JWT.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class ITokenService(ABC):
    """Abstract service xử lý JWT access token và reset token."""

    @abstractmethod
    def create_access_token(self, data: dict) -> str:
        """
        Tạo JWT access token với payload cho trước.

        Args:
            data: Dict chứa các claims (sub, email, ...).

        Returns:
            JWT string đã encode.
        """
        ...

    @abstractmethod
    def decode_token(self, token: str) -> dict:
        """
        Decode và verify JWT access token.

        Args:
            token: JWT string.

        Returns:
            Payload dict nếu hợp lệ.

        Raises:
            BusinessRuleError: Nếu token invalid hoặc hết hạn.
        """
        ...

    @abstractmethod
    def create_reset_token(self, email: str) -> str:
        """
        Tạo short-lived JWT dùng để reset mật khẩu (expire 1 giờ).

        Args:
            email: Email của hộ cần reset.

        Returns:
            JWT reset token string.
        """
        ...

    @abstractmethod
    def decode_reset_token(self, token: str) -> str:
        """
        Decode reset token và trả về email.

        Args:
            token: JWT reset token string.

        Returns:
            Email string.

        Raises:
            BusinessRuleError: Nếu token invalid, hết hạn, hoặc không phải type=reset.
        """
        ...
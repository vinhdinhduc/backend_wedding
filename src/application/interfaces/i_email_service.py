"""
Interface cho email service — gửi email qua Resend API.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class IEmailService(ABC):
    """Abstract service gửi email transactional."""

    @abstractmethod
    async def send_reset_password(self, to_email: str, reset_link: str) -> None:
        """
        Gửi email chứa link đặt lại mật khẩu.

        Args:
            to_email: Địa chỉ email người nhận.
            reset_link: URL đầy đủ dùng để reset mật khẩu (chứa token).

        Raises:
            BusinessRuleError: Nếu gửi email thất bại (log lỗi, không raise ra client).
        """
        ...
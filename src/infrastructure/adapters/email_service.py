"""
Concrete implementation của IEmailService — gửi email qua Resend API.
"""
from __future__ import annotations

import logging

import httpx

from src.application.interfaces.i_email_service import IEmailService

logger = logging.getLogger(__name__)

_RESEND_API_URL = "https://api.resend.com/emails"

_RESET_EMAIL_TEMPLATE = """
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Đặt lại mật khẩu — TienMung</title>
</head>
<body style="font-family: Arial, sans-serif; background: #f5f5f5; margin: 0; padding: 20px;">
  <div style="max-width: 520px; margin: 0 auto; background: #ffffff;
              border-radius: 8px; padding: 32px; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">

    <h2 style="color: #1a1a2e; margin-top: 0;">🔐 Đặt lại mật khẩu</h2>

    <p style="color: #444; line-height: 1.6;">
      Chúng tôi nhận được yêu cầu đặt lại mật khẩu cho tài khoản
      <strong>TienMung</strong> của bạn.
    </p>

    <p style="color: #444; line-height: 1.6;">
      Nhấn vào nút bên dưới để đặt mật khẩu mới. Link này có hiệu lực
      trong <strong>1 giờ</strong>.
    </p>

    <div style="text-align: center; margin: 32px 0;">
      <a href="{reset_link}"
         style="background: #e63946; color: #ffffff; text-decoration: none;
                padding: 14px 32px; border-radius: 6px; font-size: 16px;
                font-weight: bold; display: inline-block;">
        Đặt lại mật khẩu
      </a>
    </div>

    <p style="color: #888; font-size: 13px; line-height: 1.6;">
      Nếu bạn không yêu cầu đặt lại mật khẩu, hãy bỏ qua email này.
      Mật khẩu của bạn sẽ không thay đổi.
    </p>

    <hr style="border: none; border-top: 1px solid #eee; margin: 24px 0;">

    <p style="color: #aaa; font-size: 12px; text-align: center;">
      TienMung — Quản lý Tiền Mừng Dịch Vụ<br>
      Email này được gửi tự động, vui lòng không trả lời.
    </p>
  </div>
</body>
</html>
"""


class EmailService(IEmailService):
    """Gửi email transactional qua Resend API (httpx async)."""

    def __init__(self, api_key: str, from_email: str) -> None:
        self._api_key = api_key
        self._from_email = from_email

    async def send_reset_password(self, to_email: str, reset_link: str) -> None:
        """
        Gửi email đặt lại mật khẩu.

        Lỗi gửi email được log ở đây và KHÔNG raise ra controller
        (tránh tiết lộ trạng thái email qua timing attack).
        """
        html_body = _RESET_EMAIL_TEMPLATE.format(reset_link=reset_link)

        payload = {
            "from": self._from_email,
            "to": [to_email],
            "subject": "Đặt lại mật khẩu TienMung",
            "html": html_body,
        }

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.post(
                    _RESEND_API_URL,
                    json=payload,
                    headers={
                        "Authorization": f"Bearer {self._api_key}",
                        "Content-Type": "application/json",
                    },
                )
                response.raise_for_status()
                logger.info("Reset password email sent to %s", to_email)

        except httpx.HTTPStatusError as exc:
            logger.error(
                "Resend API error sending to %s: HTTP %s — %s",
                to_email,
                exc.response.status_code,
                exc.response.text,
            )
        except httpx.RequestError as exc:
            logger.error(
                "Network error sending reset email to %s: %s",
                to_email,
                str(exc),
            )
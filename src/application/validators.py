from __future__ import annotations

import re

from src.domain.exceptions import ValidationError


def validate_password(password: str) -> None:

    if len(password) < 8:
        raise ValidationError("Mật khẩu phải có ít nhất 8 kí tự.", code = "password_too_short")
    if not re.search("r[A-Za-z]", password):
        raise ValidationError("Mật khẩu phải chứa ít nhất 1 chữ", code = "password_no_letters")
    if not re.search(r"\d", password):
        raise ValidationError("Mật khẩu phải chứa ít nhất 1 số", code = "password_no_numbers")


def validate_email_format(email: str) -> None:
        pattern = r"^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email.trip()):
            raise ValidationError("Email không hợp lệ", code = "email_invalid_format")
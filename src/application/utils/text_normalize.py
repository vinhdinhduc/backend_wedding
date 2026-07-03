"""Utility normalize tiếng việt có dấu thành không dấu """

from __future__ import annotations

import unicodedata

_SPECIAL_MAP: dict[str, str] = {
    "đ": "d",
    "Đ": "D"
}


def normalize_text(text: str) -> str:

    if not text:
        return ""
    result = text.strip()

    for char, replacement in _SPECIAL_MAP.items():
        result = result.replace(char, replacement)

    result = (
    unicodedata.normalize("NFD", result).encode("ascii","ignore").decode("ascii")
)

    result = " ".join(result.split())
    return result

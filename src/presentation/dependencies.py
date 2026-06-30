"""Presentation dependencies helpers."""

from fastapi import Request


def get_container(request: Request):
    return getattr(request.app.state, "container", None)

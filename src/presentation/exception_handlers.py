"""Đăng kí tất cả các handler trong app factory"""

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from src.domain.exceptions import DomainException, NotFoundError, PermissionError, ValidationError, ConflictError, BusinessLogicError



def _error_response(status_code: int, message: str, code: str | None = None) -> JSONResponse:
    """Định dạng json lỗi nhất quán cho toàn bộ API"""
    content = {"details": message}
    if code:
        content["code"] = code
    return JSONResponse(status_code=status_code, content=content)

async def not_found_handler(request: Request, exc: NotFoundError) -> JSONResponse:
    return _error_response(404, exc.message, exc.code)


async def permission_handler(request: Request, exc: PermissionError) -> JSONResponse:
    return _error_response(403, exc.message, exc.code)


async def validation_handler(request: Request, exc: ValidationError) -> JSONResponse:
    return _error_response(422, exc.message, exc.code)

async def conflict_handler(request: Request, exc: ConflictError) -> JSONResponse:
    return _error_response(409, exc.message, exc.code)


async def business_rule_handler(request: Request, exc: BusinessLogicError) -> JSONResponse:
    return _error_response(400, exc.message, exc.code)

async def domain_exception_handler(request: Request, exc: DomainException) -> JSONResponse:
    return _error_response(400, exc.message, exc.code)


def register_exception_handlers(app: FastAPI) -> None:
    """Đăng kí tất cả các handler cho app"""
    app.add_exception_handler(NotFoundError, not_found_handler)
    app.add_exception_handler(PermissionError, permission_handler)
    app.add_exception_handler(ValidationError, validation_handler)
    app.add_exception_handler(ConflictError, conflict_handler)
    app.add_exception_handler(BusinessLogicError, business_rule_handler)
    app.add_exception_handler(DomainException, domain_exception_handler)

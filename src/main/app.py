"""Application factory for the wedding backend application."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.main.config import settings
from src.main.ioc.container import Container
from src.presentation.exception_handlers import register_exception_handlers


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Initialize the lightweight container and database engine on startup."""
    container = Container()
    app.state.container = container
    container.wire()

    from src.infrastructure.database.base import init_database, shutdown_database

    init_database()
    yield
    await shutdown_database()


def create_app() -> FastAPI:
    app = FastAPI(
        title="Wedding API",
        lifespan=lifespan,
        description="Hệ thống tra cứu tiền mừng và quản lý các dịch vụ khác",
        version="2.1.0",
        docs_url="/api/docs" if not settings.is_production else None,
        redoc_url="/api/redoc" if not settings.is_production else None,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    register_exception_handlers(app)
    _register_routers(app)
    return app


def _register_routers(app: FastAPI) -> None:
    from src.presentation.controllers.auth import router as auth_router

    app.include_router(auth_router)


app = create_app()
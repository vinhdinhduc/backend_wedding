from fastapi import APIRouter
from starlette import status

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register() -> dict[str, str]:
    return {"message": "Registration endpoint is ready for implementation."}


@router.post("/login", status_code=status.HTTP_200_OK)
async def login() -> dict[str, str]:
    return {"message": "Login endpoint is ready for implementation."}


@router.post("/logout", status_code=status.HTTP_200_OK)
async def logout() -> dict[str, str]:
    return {"message": "Logout endpoint is ready for implementation."}

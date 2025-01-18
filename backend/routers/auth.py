from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response

from backend.dto.auth_dto import LoginUserModel
from backend.dto.user_dto import UserModel
from backend.services.auth_service import AuthService
from backend.utils.dependencies.dependencies import (
    get_auth_service,
    get_current_user_dependency,
)

router = APIRouter(prefix="/auth", tags=["auth"])


@router.get("/current_user")
async def get_current_user(
    current_user: str = Depends(get_current_user_dependency),
) -> UserModel:
    return current_user


@router.post("/login")
async def login(
    form: LoginUserModel,
    auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> dict[str, str]:
    await auth_service.authenticate_user(**form.model_dump())
    token = await auth_service.create_access_token(**form.model_dump())
    return {"access_token": token}
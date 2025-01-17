from typing import Annotated
from fastapi import APIRouter, Depends, Request, Response

from backend.dto.user_dto import BaseUserModel
from backend.services.user_service import UserService
from backend.utils.dependencies.dependencies import (
    get_current_user_dependency,
    get_user_service,
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.get("/current_user")
async def get_current_user(
    request: Request,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: str = Depends(get_current_user_dependency),
) -> BaseUserModel:
    user = await user_service.get_user(current_user, dump=True)
    return user

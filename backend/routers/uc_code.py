from typing import Annotated
from fastapi import APIRouter, Depends

from backend.dto.activation_dto import CreateActivationModel
from backend.services.activation_service import ActivationService
from backend.services.uc_code_service import UCCodeService
from backend.utils.dependencies.dependencies import get_activation_service, get_uc_code_service


router = APIRouter(prefix="/uc_code", tags=["uc_code"])


@router.get("/all")
async def get_all_uc_codes(
    uc_code_service: Annotated[UCCodeService, Depends(get_uc_code_service)]
):
    return await uc_code_service.get_all()


@router.post("/activate")
async def activate_uc_code(
    form: CreateActivationModel,
    uc_code_service: Annotated[ActivationService, Depends(get_activation_service)],
) -> None:
    return await uc_code_service.activate_code(form)

from typing import Annotated
from fastapi import APIRouter, Depends

from backend.dto.purchase_dto import CreatePurchaseModel
from backend.dto.uc_code_dto import BuyUCCodeCallbackModel, BuyUCCodeUrlModel, UCCodeGetBuyUrlModel, UCCodeModel
from backend.dto.user_dto import UserModel
from backend.services.payment_service import PaymentService
from backend.services.purchase_service import PurchaseService
from backend.services.uc_code_service import UCCodeService
from backend.utils.dependencies.dependencies import get_current_user_dependency, get_payment_service, get_purchase_service, get_uc_code_service


router = APIRouter(prefix="/uc_code", tags=["uc_code"])


@router.get("/all")
async def get_all_uc_codes(
    uc_code_service: Annotated[UCCodeService, Depends(get_uc_code_service)]
):
    return await uc_code_service.get_all()


@router.post("/buy/callback")
async def activate_uc_code(
    form: BuyUCCodeCallbackModel,
    payment_service: Annotated[PaymentService, Depends(get_payment_service)],
    purchase_service: Annotated[PurchaseService, Depends(get_purchase_service)],
) -> None:
    await payment_service.activate_code(form)
    return await purchase_service.mark_is_paid(form.order_id)



@router.post("/buy/url")
async def get_byu_uc_code_url(
    form: UCCodeGetBuyUrlModel,
    payment_service: Annotated[PaymentService, Depends(get_payment_service)],
    purchase_service: Annotated[PurchaseService, Depends(get_purchase_service)],
    current_user: UserModel = Depends(get_current_user_dependency),
) -> BuyUCCodeUrlModel:
    response = await payment_service.get_payment_url(
        form,
        tg_id=current_user.tg_id
    )
    await purchase_service.create_purchase(
        CreatePurchaseModel(
            payment_id=response.order_id,
            uc_sum=form.amount,
            payment_method=form.method_slug,
            player_id=form.player_id,
            metadata_={
                "tg_id": current_user.tg_id,
                "uc_packs": form.uc_packs
            }
        )
    )
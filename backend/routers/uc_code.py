from typing import Annotated
from fastapi import APIRouter, Depends

from backend.dto.purchase_dto import CreatePurchaseModel, PurchaseModel
from backend.dto.uc_code_dto import BuyUCCodeCallbackModel, BuyUCCodeUrlModel, PaymentUCCodeDataModel, UCCodeGetBuyUrlModel, UCCodeModel
from backend.dto.user_dto import UserModel
from backend.services.payment_service import PaymentService
from backend.services.purchase_service import PurchaseService
from backend.services.uc_code_service import UCCodeService
from backend.services.user_service import UserService
from backend.utils.dependencies.dependencies import (
    get_current_user_dependency, 
    get_payment_service, 
    get_purchase_service, 
    get_uc_code_service, 
    get_user_service
)


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
    uc_code_service: Annotated[UCCodeService, Depends(get_uc_code_service)],
    purchase_service: Annotated[PurchaseService, Depends(get_purchase_service)],
    user_service: Annotated[UserService, Depends(get_user_service)]
) -> PurchaseModel:
    purchase = await purchase_service.mark_is_paid(form.order_id, form.metadata.internal_order_id)
    await payment_service.activate_codes(form)
    bonuses = await uc_code_service.get_uc_packs_bonuses_sum(form.metadata.uc_packs)
    await user_service.send_bonuses_to_referer(form.metadata.tg_id, bonuses)
    return purchase


@router.post("/buy/url")
async def get_byu_uc_code_url(
    form: UCCodeGetBuyUrlModel,
    payment_service: Annotated[PaymentService, Depends(get_payment_service)],
    purchase_service: Annotated[PurchaseService, Depends(get_purchase_service)],
    current_user: UserModel = Depends(get_current_user_dependency),
) -> PaymentUCCodeDataModel:
    response = await payment_service.get_payment_url(
        form,
        tg_id=current_user.tg_id
    )
    return await purchase_service.create_purchase(
        CreatePurchaseModel(
            tg_id=current_user.tg_id,
            payment_id=response.order_id,
            internal_order_id=response.internal_id,
            uc_sum=form.uc_sum,
            price=form.amount,
            payment_method=form.method_slug,
            player_id=form.player_id,
            metadata_={
                "tg_id": current_user.tg_id,
                "uc_packs": form.uc_packs
            }
        ),
        codeepay_response=response
    )
import asyncio
import json
from typing import Annotated
from fastapi import APIRouter, BackgroundTasks, Depends, WebSocket

from backend.dto.uc_code_dto import CodeepayBuyUCCodeCallbackModel, BuyUCCodeUrlModel, UCCodeGetBuyUrlModel
from backend.dto.user_dto import UserModel
from backend.services.discount_service import DiscountService
from backend.services.payment_service import PaymentService
from backend.services.purchase_service import PurchaseService
from backend.services.setting_service import SettingService
from backend.services.uc_code_service import UCCodeService
from backend.services.user_service import UserService
from backend.utils.config.enums import BuyServices
from backend.utils.dependencies.dependencies import (
    get_current_user_dependency,
    get_discount_service, 
    get_payment_service, 
    get_purchase_service,
    get_setting_service, 
    get_uc_code_service, 
    get_user_service,
    get_websocket_manager
)
from backend.utils.websocket.manager import WebsocketManager


router = APIRouter(prefix="/uc_code", tags=["uc_code"])


@router.get("/all")
async def get_all_uc_codes(
    uc_code_service: Annotated[UCCodeService, Depends(get_uc_code_service)]
):
    return await uc_code_service.group_by_amount()


@router.post("/buy/callback")
@router.get("/buy/callback")
async def activate_uc_code(
    payment_service: Annotated[PaymentService, Depends(get_payment_service)],
    uc_code_service: Annotated[UCCodeService, Depends(get_uc_code_service)],
    purchase_service: Annotated[PurchaseService, Depends(get_purchase_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    setting_service: Annotated[SettingService, Depends(get_setting_service)],
    form: CodeepayBuyUCCodeCallbackModel | None = None,
    intid: int | None = None,
):
    # service = await setting_service.get_self_payment_service()
    all_activated = False
    try:
        service = BuyServices.CODEEPAY.value if form else BuyServices.FREEKASSA.value 
        if service == BuyServices.CODEEPAY.value:
            purchase = await purchase_service.get_by_order_id(form.order_id)
        elif service == BuyServices.FREEKASSA.value:
            purchase = await purchase_service.get_by_order_id(str(intid))
        if purchase.is_paid:
            return 
        adding_bonuses = await uc_code_service.get_uc_packs_bonuses_sum(
            json.loads(purchase.metadata_).get("uc_packs")
        )
        if service == BuyServices.CODEEPAY.value:
            purchase = await purchase_service.get_by_order_id(form.order_id)
        elif service == BuyServices.FREEKASSA.value:
            purchase = await purchase_service.get_by_order_id(str(intid))
        all_activated, metadata = await payment_service.activate_codes(purchase, player_id)
        purchase = await purchase_service.mark_is_paid(
            purchase.payment_id, 
            form.metadata.internal_order_id if service == BuyServices.CODEEPAY.value else purchase.internal_order_id,
            metadata,
            all_activated
        )
        await user_service.send_bonuses_to_referer(purchase.tg_id, adding_bonuses)
    except Exception as e:
        raise e
    finally:
        if service == BuyServices.CODEEPAY.value:
            purchase = await purchase_service.get_by_order_id(form.order_id)
        elif service == BuyServices.FREEKASSA.value:
            purchase = await purchase_service.get_by_order_id(str(intid))
        user = await user_service.get_user(purchase.tg_id)
        await payment_service.send_payment_notification(purchase, all_activated, user.username)


@router.post("/buy/url")
async def get_buy_uc_code_url(
    form: UCCodeGetBuyUrlModel,
    payment_service: Annotated[PaymentService, Depends(get_payment_service)],
    setting_service: Annotated[SettingService, Depends(get_setting_service)],
    purchase_service: Annotated[PurchaseService, Depends(get_purchase_service)],
    discount_service: Annotated[DiscountService, Depends(get_discount_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    uc_code_service: Annotated[UCCodeService, Depends(get_uc_code_service)],
    current_user: UserModel = Depends(get_current_user_dependency)
) -> BuyUCCodeUrlModel: 
    # service = await setting_service.get_self_payment_service()
    service = BuyServices.CODEEPAY.value if form.method_slug == "card" else BuyServices.FREEKASSA.value 
    await uc_code_service.check_packs(form.uc_packs, form.uc_sum, form.amount)
    if form.discount:
        form.discount = await discount_service.delete_discount_from_user(current_user.tg_id, form.discount)
    await user_service.check_player_id(form.player_id)
    last_purchase_id = (
        await setting_service.get_last_purchase_id() 
        if BuyServices.FREEKASSA.value == service 
        else None
    )
    response = await payment_service.get_uc_payment_url(form, current_user.tg_id, service, last_purchase_id)
    await purchase_service.create_purchase(form, current_user, response)
    return response


@router.websocket("/buy/status/{order_id}")
async def uc_code_status_checker(
    websocket: WebSocket,
    order_id: str,
    purchase_service: Annotated[PurchaseService, Depends(get_purchase_service)],
    manager: Annotated[WebsocketManager, Depends(get_websocket_manager)],
) -> None:
    await manager.connect(order_id, websocket)
    try:
        max_retries = 30
        while True:
            if websocket.client_state.name != "CONNECTED":
                break
            elif max_retries == 0:
                break

            is_paid_response = await purchase_service.check_is_paid(order_id)
            if is_paid_response:    
                await manager.send_message(order_id, is_paid_response, event="purchase_status")
                break
            else:
                await asyncio.sleep(1)
            max_retries -= 1
    except Exception as e:
        await manager.send_message(order_id, {"error": str(e)}, event="purchase_status")
        raise e
    finally:
        await manager.disconnect(order_id)
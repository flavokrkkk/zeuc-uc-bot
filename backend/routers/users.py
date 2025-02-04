from typing import Annotated
from fastapi import APIRouter, Depends
from starlette.responses import JSONResponse

from backend.dto.purchase_dto import PurchaseModel
from backend.dto.reward import DiscountModel, UpdateUserRewardsModel
from backend.dto.uc_code_dto import BuyPointCallbackModel, BuyPointModel
from backend.dto.user_dto import BonusesHistoryModel, UserModel
from backend.services.discount_service import DiscountService
from backend.services.payment_service import PaymentService
from backend.services.purchase_service import PurchaseService
from backend.services.reward_service import RewardService
from backend.services.user_service import UserService
from backend.utils.dependencies.dependencies import (
    get_current_user_dependency,
    get_discount_service,
    get_payment_service,
    get_purchase_service,
    get_reward_service,
    get_user_service
)


router = APIRouter(prefix="/user", tags=["users"])


@router.post("/rewards")
async def update_user_rewards(
    form: UpdateUserRewardsModel,
    reward_service: Annotated[RewardService, Depends(get_reward_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    payment_service: Annotated[PaymentService, Depends(get_payment_service)],
    current_user: UserModel = Depends(get_current_user_dependency),
) -> JSONResponse:
    await user_service.check_user_balance(current_user)
    reward, response = await reward_service.get_winned_reward(form.reward_id)
    if reward.reward_type == "uc_code": 
        await payment_service.activate_code_without_callback(
            reward.uc_amount, 
            form.player_id
        )
    else:
        await user_service.update_rewards(current_user, reward)
    return response


@router.get("/discounts")
async def get_user_discounts(
    discount_service: Annotated[DiscountService, Depends(get_discount_service)],
    current_user: UserModel = Depends(get_current_user_dependency),
) -> list[DiscountModel]:
    return await discount_service.get_user_discounts(current_user.tg_id)


@router.patch("/referal_code/{referal_code}/activate")
async def activate_referal_code(
    referal_code: str,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: UserModel = Depends(get_current_user_dependency),
) -> JSONResponse:
    return await user_service.activate_referal_code(current_user, referal_code)


@router.get("/purchases")
async def get_user_purchases(
    purchase_service: Annotated[PurchaseService, Depends(get_purchase_service)],
    current_user: UserModel = Depends(get_current_user_dependency),
) -> list[PurchaseModel]:
    return await purchase_service.get_by_tg_id(current_user.tg_id)


@router.get("/bonuses/history")
async def get_user_bonuses_history(
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: UserModel = Depends(get_current_user_dependency),
) -> list[BonusesHistoryModel]:
    return await user_service.get_user_bonuses_history(current_user.tg_id)


@router.post("/buy/points")
async def get_buy_points_url(
    form: BuyPointModel, 
    payment_service: Annotated[PaymentService, Depends(get_payment_service)],
    current_user: UserModel = Depends(get_current_user_dependency)
) -> str:
    return await payment_service.get_point_payment_url(form, current_user.tg_id)


@router.post("/buy/point/callback")
async def buy_points_callback(
    form: BuyPointCallbackModel, 
    user_service: Annotated[UserService, Depends(get_user_service)],
) -> JSONResponse:
    return await user_service.add_bonuses(form)
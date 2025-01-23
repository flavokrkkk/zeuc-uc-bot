from typing import Annotated
from fastapi import APIRouter, Depends

from backend.dto.reward import UpdateUserRewardsModel
from backend.dto.user_dto import UserModel
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
):
    reward = await reward_service.get_reward(form.reward_id, dump=False)
    if reward.reward_type == "uc_code":
        return await payment_service.activate_code_without_callback(reward.uc_code, form.player_id)
    return await user_service.update_rewards(current_user, reward)


@router.get("/discounts")
async def get_user_discounts(
    discount_service: Annotated[DiscountService, Depends(get_discount_service)],
    current_user: UserModel = Depends(get_current_user_dependency),
):
    return await discount_service.get_user_discounts(current_user.tg_id)


@router.patch("/referal_code/{referal_code}/activate")
async def activate_referal_code(
    referal_code: str,
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: UserModel = Depends(get_current_user_dependency),
):
    return await user_service.activate_referal_code(current_user, referal_code)


@router.get("/purchases")
async def get_user_purchases(
    purchase_service: Annotated[PurchaseService, Depends(get_purchase_service)],
    current_user: UserModel = Depends(get_current_user_dependency),
):
    return await purchase_service.get_by_tg_id(current_user.tg_id)


@router.get("/bonuses/history")
async def get_user_bonuses_history(
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: UserModel = Depends(get_current_user_dependency),
):
    return await user_service.get_user_bonuses_history(current_user.tg_id)
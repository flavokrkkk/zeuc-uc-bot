from typing import Annotated
from fastapi import APIRouter, Depends

from backend.dto.user_dto import UserModel
from backend.services.discount_service import DiscountService
from backend.services.reward_service import RewardService
from backend.services.user_service import UserService
from backend.utils.dependencies.dependencies import get_current_user_dependency, get_discount_service, get_reward_service, get_user_service


router = APIRouter(prefix="/user", tags=["users"])


@router.post("/rewards/{reward_id}")
async def update_user_rewards(
    reward_id: int,
    reward_service: Annotated[RewardService, Depends(get_reward_service)],
    user_service: Annotated[UserService, Depends(get_user_service)],
    current_user: UserModel = Depends(get_current_user_dependency),
):
    reward = await reward_service.get_reward(reward_id, dump=False)
    return await user_service.update_rewards(current_user.tg_id, reward)


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
    return await user_service.activate_referal_code(
        current_user.tg_id, 
        referal_code, 
        current_user.bonuses
    )
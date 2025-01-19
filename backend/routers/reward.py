from typing import Annotated
from fastapi import APIRouter, Depends

from backend.services.reward_service import RewardService
from backend.utils.dependencies.dependencies import get_reward_service


router = APIRouter(prefix="/reward", tags=["reward"])


@router.get("/all")
async def get_all_rewards(
    reward_service: Annotated[RewardService, Depends(get_reward_service)],
):
    return await reward_service.get_rewards()

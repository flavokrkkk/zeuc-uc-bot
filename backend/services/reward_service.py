from starlette.responses import JSONResponse
from backend.database.models.models import Reward
from backend.dto.reward import RewardModel
from backend.errors.reward_errors import RewardCantBeTaken
from backend.repositories.reward_repository import RewardRepository


class RewardService:
    def __init__(self, repository: RewardRepository):
        self.repository = repository

    async def get_reward(self, reward_id: int, dump: bool = True) -> RewardModel:
        reward = await self.repository.get_item(reward_id)
        return RewardModel.model_validate(reward, from_attributes=True) if dump else reward
    
    async def get_winned_reward(self, user_id: int, reward_id: int, rewards_key: str) -> tuple[Reward, JSONResponse]:
        is_activated = await self.repository.activate_reward(user_id, reward_id, rewards_key)
        if not is_activated:
            raise RewardCantBeTaken
        
        reward = await self.get_reward(reward_id, dump=False)
        return reward, JSONResponse(
            status_code=200,
            content={
                "message": (
                    f"Вы выиграли скидку {reward.discount.value}"
                    f"при покупке от {reward.discount.min_payment_value} рублей"
                ) if reward.reward_type == "discount" else (
                    f"Вы выиграли {reward.uc_amount} UC"
                )
            }
        )

    async def get_rewards(self) -> list[dict]:
        rewards = await self.repository.get_all_items()
        return [
            RewardModel
            .model_validate(reward, from_attributes=True)
            .model_dump(exclude_none=True) 
            for reward in rewards
        ]

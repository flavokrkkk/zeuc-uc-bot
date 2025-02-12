from sqlalchemy import select
from backend.database.models.models import Reward, UserRewards
from backend.repositories.base import SqlAlchemyRepository


class RewardRepository(SqlAlchemyRepository):
    model = Reward

    async def activate_reward(self, user_id: int, reward_id: int, rewards_key: str) -> None:
        query = select(UserRewards).where(
            UserRewards.user_id == user_id,
            UserRewards.secret_key == rewards_key
        )
        user_reward = await self.session.execute(query)
        user_reward = user_reward.scalar_one_or_none()
        if user_reward and not user_reward.is_used:
            user_reward.is_used = True
            user_reward.reward_id = reward_id
            await self.session.commit()
            return True
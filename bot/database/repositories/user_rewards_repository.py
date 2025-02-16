from sqlalchemy import func, select
from database.models.models import UserRewards
from database.repositories.base import SqlAlchemyRepository


class UserRewardsRepository(SqlAlchemyRepository):
    model = UserRewards

    async def get_user_rewards_pages(self, user_id: int) -> int | None:
        pages_query = select(func.count()).select_from(UserRewards).where(UserRewards.user_id == user_id)
        pages = (await self.session.execute(pages_query)).scalar()
        return pages // 10 if pages // 10 else None

    async def get_user_rewards(self, tg_id: str, page: int) -> list[UserRewards]:
        query = (
            select(UserRewards)
            .where(self.model.user_id == tg_id, UserRewards.reward_id.is_not(None))
            .limit(10)
            .offset(page * 10)
        )
        return (await self.session.execute(query)).scalars().all()
    
    async def get_user_rewards_by_date(self, start_date: int, end_date: int, page: int) -> list[UserRewards]:
        query = (
            select(UserRewards)
            .where(UserRewards.created_at.between(start_date, end_date))
            .limit(10)
            .offset(page * 10)
        )
        return (await self.session.execute(query)).scalars().all()
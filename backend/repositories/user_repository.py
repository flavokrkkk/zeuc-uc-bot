from sqlalchemy import select

from backend.database.models.models import User, UserRewards
from backend.database.models.models import BonusesHistory, UserDiscounts
from backend.repositories.base import SqlAlchemyRepository
from backend.utils.config.enums import BonusStatuses


class UserRepository(SqlAlchemyRepository):
    model = User

    async def add_discount(self, tg_id: int, discount_id: int) -> None:
        user_discount = (
            await self.session.execute(
                select(UserDiscounts)
                .where(UserDiscounts.user_id == tg_id)
                .where(UserDiscounts.discount_id == discount_id)
            )
        ).scalar_one_or_none()

        if user_discount is not None:
            user_discount.count += 1
            return await self.session.commit()

        user_discount = UserDiscounts(user_id=tg_id, discount_id=discount_id)
        self.session.add(user_discount)
        await self.session.commit()

    async def update_bonuses(self, tg_id: int, bonuses: int, status: str) -> None:
        user: User = await self.get_item(tg_id)
        if status == BonusStatuses.GET.value:
            user.bonuses += bonuses
        elif user.bonuses - bonuses >= 0 and status == BonusStatuses.USE.value:
            user.bonuses -= bonuses
        else:
            return 
        user.bonuses_history.append(
            BonusesHistory(tg_id=tg_id, amount=bonuses, status=status)
        )
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def create_user_reward(self, user_id: int, secret_key: str) -> None:
        user_reward = UserRewards(user_id=user_id, secret_key=secret_key)
        self.session.add(user_reward)
        await self.session.commit()
        await self.session.refresh(user_reward)
        return user_reward
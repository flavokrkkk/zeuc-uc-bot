from sqlalchemy import select, update

from backend.database.models import User
from backend.database.models.models import BonusesHistory, UserDiscounts
from backend.repositories.base import SqlAlchemyRepository


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

    async def add_bonuses(self, tg_id: int, bonuses: int, status: str) -> None:
        user: User = await self.get_item(tg_id)
        user.bonuses += bonuses
        user.bonuses_history.append(
            BonusesHistory(tg_id=tg_id, amount=bonuses, status=status)
        )
        await self.session.commit()
        
from sqlalchemy import select
from backend.database.models.models import Discount, UserDiscounts
from backend.repositories.base import SqlAlchemyRepository


class DiscountRepository(SqlAlchemyRepository):
    model = Discount
    
    async def get_user_discounts(self, tg_id: int) -> list[Discount]:
        return (
            await self.session.execute(
                select(UserDiscounts)
                .where(UserDiscounts.user_id == tg_id)
            )
        ).scalars().all()
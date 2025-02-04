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
    
    async def delete_discount_from_user(self, tg_id: int, discount_id: int) -> int | None:
        query = select(UserDiscounts).where(
            UserDiscounts.user_id == tg_id,
            UserDiscounts.discount_id == discount_id
        )
        user_discount = (await self.session.execute(query)).scalar_one_or_none()
        
        if not user_discount:
            return
        
        discount = await self.get_item(discount_id)
        discount_value = 0
        if user_discount.count - 1 == 0:
            discount_value = discount.value
            await self.session.delete(user_discount)
        else: 
            user_discount.count -= 1
            discount_value = discount.value 
        await self.session.commit()
        return discount_value
    
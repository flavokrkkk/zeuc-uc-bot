from sqlalchemy import select
from database.models.models import Discount
from database.repositories.base import SqlAlchemyRepository


class DiscountRepository(SqlAlchemyRepository):
    model = Discount

    async def get_by_value(self, value: int):
        query = select(self.model).where(self.model.value == value)
        return (await self.session.execute(query)).scalar_one_or_none()
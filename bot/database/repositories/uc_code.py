from sqlalchemy import func, select
from database.models.models import UCCode
from database.repositories.base import SqlAlchemyRepository


class UCCodeRepository(SqlAlchemyRepository):
    model = UCCode

    async def group_by_amount(self):
        query = (
            select(
                self.model.uc_amount,
                func.count(self.model.uc_amount).label("count")
            )
            .group_by(self.model.uc_amount)
            .order_by(self.model.uc_amount)
        )
        uc_codes = await self.session.execute(query)
        return uc_codes.all()
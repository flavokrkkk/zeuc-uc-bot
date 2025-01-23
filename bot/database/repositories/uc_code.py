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
    
    async def get_count_by_amount(self, uc_amount: int):
        query = (
            select(func.count(self.model.uc_amount))
            .where(self.model.uc_amount == uc_amount)
        )
        uc_codes = (await self.session.execute(query)).scalar()
        return uc_codes

    async def delete_codes_by_value(self, uc_amount: int, quantity: int):
        query = (
            select(self.model)
            .where(self.model.uc_amount == uc_amount)
            .limit(quantity)
        )
        uc_codes = (await self.session.execute(query)).scalars().all()
        returning_codes = [uc_code.code for uc_code in uc_codes]

        for uc_code in uc_codes:
            await self.session.delete(uc_code)

        await self.session.commit()
        return returning_codes
    
    async def add_new_codes(self, new_uc_codes: list[str], uc_amount: int):
        for uc_code in new_uc_codes:
            await self.add_item(code=uc_code, uc_amount=uc_amount)
        
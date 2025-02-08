from sqlalchemy import func, select
from database.models.models import Price, UCCode
from database.repositories.base import SqlAlchemyRepository


class UCCodeRepository(SqlAlchemyRepository):
    model = UCCode

    async def group_by_amount(self) -> list[tuple[int, int]]:
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
    
    async def get_count_by_amount(self, uc_amount: int) -> int:
        query = (
            select(func.count(self.model.uc_amount))
            .where(self.model.uc_amount == uc_amount)
        )
        uc_codes = (await self.session.execute(query)).scalar()
        return uc_codes

    async def delete_codes_by_value(self, uc_amount: int, quantity: int) -> list[str]:
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
    
    async def add_new_codes(
        self, 
        new_uc_codes: list[str], 
        uc_amount: int, 
        price_per_uc: int, 
        point: int
    ) -> None:
        price = Price(price=price_per_uc, point=point)
        uc_codes = [
            UCCode(code=uc_code, uc_amount=uc_amount) 
            for uc_code in new_uc_codes
        ]
        price.uc_codes.extend(uc_codes)
        self.session.add(price)
        await self.session.commit()
        
    async def change_price(self, uc_amount: str, new_price: float) -> None:
        query = select(Price).where(Price.uc_codes.any(uc_amount=uc_amount))
        price = (await self.session.execute(query)).scalar_one_or_none()
        price.price = new_price
        await self.session.commit()
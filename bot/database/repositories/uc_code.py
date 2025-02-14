from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from database.models.models import Price, UCCode
from database.repositories.base import SqlAlchemyRepository


class UCCodeRepository(SqlAlchemyRepository):
    model = UCCode

    async def group_by_amount(self) -> list[tuple[int, int]]:
        query = select(Price).options(selectinload(Price.uc_codes))
        prices: list[Price] = (await self.session.execute(query)).scalars().all()
        return [
            [price.uc_amount, len(price.uc_codes)]
            for price in prices
        ]
    
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
    
    async def add_uc_pack(
        self, 
        new_uc_codes: list[str], 
        uc_amount: int, 
        price_per_uc: int, 
        point: int
    ) -> None:
        price = Price(price=price_per_uc, point=point, uc_amount=uc_amount)
        uc_codes = [
            UCCode(code=uc_code, uc_amount=uc_amount) 
            for uc_code in new_uc_codes
        ]
        price.uc_codes.extend(uc_codes)
        self.session.add(price)
        await self.session.commit()
        
    async def change_price(self, uc_amount: str, new_price: float) -> None:
        query = select(Price).where(Price.uc_amount == uc_amount)
        price = (await self.session.execute(query)).scalar_one_or_none()
        price.price = new_price
        await self.session.commit()

    async def add_new_codes(self, uc_codes: list[str], uc_amount: int) -> None:
        price_query = select(Price).where(Price.uc_amount == uc_amount)
        price = (await self.session.execute(price_query)).scalar_one_or_none()
        new_uc_codes = [
            UCCode(price_id=price.price_id, uc_amount=uc_amount, code=uc_code)
            for uc_code in uc_codes
        ]
        self.session.add_all(new_uc_codes)
        await self.session.commit()

    async def change_point(self, uc_amount: int, point: int) -> None:
        query = select(Price).where(Price.uc_amount == uc_amount)
        price = (await self.session.execute(query)).scalar_one_or_none()
        price.point = point 
        await self.session.commit()
        
    async def get_price_by_amount(self, uc_amount: int) -> Price:
        query = select(Price).where(Price.uc_amount == uc_amount)
        price = (await self.session.execute(query)).scalar_one_or_none()
        return price
from sqlalchemy.orm import selectinload
from backend.database.models.models import Price, UCCode
from backend.repositories.base import SqlAlchemyRepository
from sqlalchemy import select, func


class UCCodeRepository(SqlAlchemyRepository):
    model = UCCode

    async def activate_code(self, code: str):
        uc_code = await self.get_item(code)
        await self.delete_item(uc_code)

    async def group_by_amount(self):
        query = select(Price).options(selectinload(Price.uc_codes))
        prices: list[Price] = (await self.session.execute(query)).scalars().all()
        return [
            [price.uc_amount, price.price, len(price.uc_codes), price.point]
            for price in prices
        ]
    
    async def get_activating_codes(self, uc_amount: int, quantity: int) -> list[str]:
        query = (
            select(self.model)
            .where(self.model.uc_amount == uc_amount)
            .limit(quantity)
        )
        db_uc_codes = (await self.session.execute(query)).scalars().all()
        uc_codes = [uc_code.code for uc_code in db_uc_codes]
        for uc_code in db_uc_codes:
            await self.delete_item(uc_code)
        return uc_codes
    
    async def return_back_uc_code(self, code: str, uc_amount: int, price: float):
        uc_code = UCCode(
            code=code, 
            uc_amount=uc_amount, 
            price_id=(
                select(Price.price_id)
                .where(Price.price == price)
                .limit(1)
                .scalar_subquery()
            )
        )
        self.session.add(uc_code)
        await self.session.commit()

    async def get_point_by_uc_amount(self, uc_amount: int) -> float:
        query = (
            select(Price.point)
            .join(UCCode, Price.price_id == UCCode.price_id)
            .where(UCCode.uc_amount == uc_amount)
            .limit(1)
        )
        price = (await self.session.execute(query)).scalar_one_or_none()
        return price
    
    async def get_activating_code(self, uc_amount: int) -> UCCode:
        query = (
            select(self.model)
            .where(self.model.uc_amount == uc_amount)
            .limit(1)
        )
        uc_code = (await self.session.execute(query)).scalar_one_or_none()
        return uc_code
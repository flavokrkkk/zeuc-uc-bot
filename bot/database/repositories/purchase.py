from collections import defaultdict
import json

from sqlalchemy import func, select, update
from database.models.models import Purchase
from database.repositories.base import SqlAlchemyRepository


class PurchaseRepository(SqlAlchemyRepository):
    model = Purchase

    async def get_stats(self, start_date: int = None, end_date: int = None) -> dict[str, int]:
        if start_date and end_date:
            query = select(self.model.metadata_).where(
                self.model.created_at.between(start_date, end_date)
            )
        else:
            query = select(self.model.metadata_)
        
        metadata_list = (await self.session.execute(query)).scalars().all()
        stats = defaultdict(int)

        for metadata in metadata_list:
            metadata = json.loads(metadata)
            uc_pack = metadata["uc_packs"]
            
            for pack in uc_pack:
                uc_amount = pack["uc_amount"]
                count = pack["quantity"]
                stats[uc_amount] += count

        return stats
    
    async def get_users_who_buyed(self) -> int:
        query = select(func.count(func.distinct(Purchase.tg_id)))
        result = await self.session.execute(query)
        unique_buyers_count = result.scalar() 
        return unique_buyers_count
    
    async def get_by_order_id(self, order_id: str) -> Purchase:
        query = select(self.model).where(self.model.payment_id == order_id)
        return (await self.session.execute(query)).scalar_one_or_none()
    
    async def set_status(self, order_id: str, status: str) -> Purchase:
        query = (
            update(self.model)
            .where(self.model.payment_id == order_id)
            .values(status=status)
            .returning(self.model)
        )
        item = (await self.session.execute(query)).scalar_one_or_none()
        await self.session.commit()
        await self.session.refresh(item)
        return item

    async def get_pages_by_date(self, start_date: int, end_date: int) -> int | None:
        pages_query = (
            select(func.count())
            .select_from(self.model)
            .where(self.model.created_at.between(start_date, end_date))
        )
        pages = (await self.session.execute(pages_query)).scalar()
        return pages // 10 if pages // 10 else 0
    
    async def get_by_date(self, start_date: int, end_date: int, page: int) -> list[Purchase]:
        query = (
            select(self.model)
            .where(self.model.created_at.between(start_date, end_date))
            .limit(10)
            .offset(page * 10)
            .order_by(self.model.created_at.desc())
        )
        return (await self.session.execute(query)).scalars().all() 
    
    async def get_total_sum(self): 
        query = select(func.sum(self.model.price))
        return (await self.session.execute(query)).scalar()
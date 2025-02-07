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

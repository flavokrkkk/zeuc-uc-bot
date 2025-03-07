from sqlalchemy import select
from backend.database.models.models import Setting
from backend.repositories.base import SqlAlchemyRepository


class SettingRepository(SqlAlchemyRepository):
    model = Setting

    async def get_item(self) -> Setting:
        query = select(self.model)
        return (await self.session.execute(query)).scalar_one_or_none()
    
    async def get_last_purchase_id(self) -> int:
        setting = await self.get_item()
        setting.last_purchase_id += 1
        await self.session.commit()
        await self.session.refresh(setting)
        return setting.last_purchase_id
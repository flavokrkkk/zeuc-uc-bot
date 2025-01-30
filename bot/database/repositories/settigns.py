from sqlalchemy import select
from database.models.models import Setting
from database.repositories.base import SqlAlchemyRepository


class SettingsRepository(SqlAlchemyRepository):
    model = Setting

    async def get_item(self):
        query = select(self.model)
        setting = (await self.session.execute(query)).scalar_one_or_none()
        return setting
    
    async def get_store_is_on(self):
        store = await self.get_item()
        return store.store_is_on
    
    async def update_store_is_on(self):
        setting = await self.get_item()

        store_is_on = not setting.store_is_on
        setting.store_is_on = store_is_on
        await self.session.commit()
        return store_is_on
    
        
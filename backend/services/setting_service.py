from backend.errors.setting_errors import StoreIsOffError
from backend.repositories.setting_repository import SettingRepository


class SettingService:
    def __init__(self, repository: SettingRepository):
        self.repository = repository
        
    async def check_store_is_on(self):
        setting = await self.repository.get_item()
        if setting.store_is_on:
            return True
        raise StoreIsOffError
    
    async def get_last_purchase_id(self):
        return await self.repository.get_last_purchase_id()
    
    async def get_self_payment_service(self):
        setting = await self.repository.get_item()
        return setting.payment_service
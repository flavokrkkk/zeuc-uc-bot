from backend.errors.setting_errors import StoreIsOffError
from backend.repositories.setting_repository import SettingRepository


class SettingService:
    def __init__(self, setting_repository: SettingRepository):
        self.setting_repository = setting_repository
        
    async def check_store_is_on(self):
        setting = await self.setting_repository.get_item()
        if setting.store_is_on:
            return True
        raise StoreIsOffError
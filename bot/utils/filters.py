from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery

from database.db_main import Database


class IsAdminFilter(BaseFilter):
    async def __call__(self, callback: CallbackQuery, database: Database) -> bool:
        user_id = callback.from_user.id
        user = await database.users.get_item(user_id) 
        return user.is_admin
    
from pprint import pprint
from typing import Callable, Awaitable, Any, Dict

from aiogram import BaseMiddleware
from aiogram.types import  CallbackQuery, Message, TelegramObject, Update

from database.connection.pg_connection import DatabaseConnection
from database.db_main import Database


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        try:
            session = await self.db_connection.get_session()
            database = Database(session=session)
            data['database'] = database
            
            if event.message.text and event.message.text == "/start":
                return await handler(event, data)
            user_data = data["event_from_user"]
            user_in_db = await database.users.get_item(item_id=user_data.id)
            
            if user_in_db != user_data["username"]:
                await database.users.update_item(
                    item_id=user_data.id,
                    username=user_data.username
                )
            return await handler(event, data)
        finally:
            await session.close()

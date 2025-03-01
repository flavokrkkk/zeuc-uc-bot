from pprint import pprint
from random import randint
from secrets import choice
from string import ascii_letters, digits
from typing import Callable, Awaitable, Any, Dict

from aiogram import BaseMiddleware
from aiogram.types import  CallbackQuery, Message, TelegramObject, Update

from database.models.models import User
from database.connection.pg_connection import DatabaseConnection
from database.db_main import Database


class DatabaseMiddleware(BaseMiddleware):
    def __init__(self, db_connection: DatabaseConnection):
        self.db_connection = db_connection

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: Update,
        data: Dict[str, Any]
    ) -> Any:
        try:
            session = await self.db_connection.get_session()
            database = Database(session=session)

            data['database'] = database
                        
            store_is_on = await database.settings.get_store_is_on()
            if not store_is_on and event.message and event.message.text != "/admin":
                if event.callback_query:
                    return await event.callback_query.message.edit_text("Магазин выключен")
                return await event.message.answer("Магазин выключен")
            
            user_data = data["event_from_user"]
            user_in_db: User = await database.users.get_item(item_id=user_data.id)

            if not user_in_db:
                await database.users.add_item(
                    tg_id=user_data.id, 
                    username=user_data.username
                )
            if not user_in_db.username or not user_data.username:
                length = randint(8, 10)
                random_string = ''.join(choice(ascii_letters + digits) for _ in range(length))
                await database.users.update_item(
                    User.tg_id,
                    user_data.id,
                    username=f"user_{random_string}"
                )
            elif user_in_db.username != user_data.username:
                await database.users.update_item(
                    User.tg_id,
                    user_data.id,
                    username=user_data.username
                )
            return await handler(event, data)
        finally:
            await session.close()

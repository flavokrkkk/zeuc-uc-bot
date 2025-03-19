from pprint import pprint
from random import randint
from secrets import choice
from string import ascii_letters, digits
from typing import Callable, Awaitable, Any, Dict

from aiogram import BaseMiddleware
from aiogram.types import  CallbackQuery, Message, TelegramObject, Update
from passlib import exc

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
                username = user_data.username if user_data.username else str(user_data.id)
                await database.users.add_item(
                    tg_id=user_data.id,
                    username=username
                )
            else:
                expected_username = user_data.username if user_data.username else str(user_data.id)
                if user_in_db.username != expected_username:
                    await database.users.update_item(
                        User.tg_id,
                        user_data.id,
                        username=expected_username
                    )
            return await handler(event, data)
        except Exception as e:
            print(e)
        finally:
            await session.close()

import logging
import asyncio

from aiogram import Bot, Dispatcher

from database.connection.pg_connection import DatabaseConnection
from middleware.db_middleware import DatabaseMiddleware
from handlers import router
from config import bot_config
from keyboards.commands import set_bot_commands


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    bot = Bot(token=bot_config.BOT_TOKEN)
    dp = Dispatcher()

    await set_bot_commands(bot)

    dp.include_router(router)
    dp.update.middleware(DatabaseMiddleware(db_connection=DatabaseConnection()))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

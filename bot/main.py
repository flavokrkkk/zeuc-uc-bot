import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from database.connection.pg_connection import DatabaseConnection
from middleware.db_middleware import DatabaseMiddleware
from handlers import router
from utils.config.config import bot_config
from keyboards.commands import set_bot_commands


async def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    bot = Bot(
        token=bot_config.BOT_TOKEN, 
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    dp = Dispatcher()

    await set_bot_commands(bot)

    dp.include_router(router)
    dp.update.middleware(DatabaseMiddleware(db_connection=DatabaseConnection()))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

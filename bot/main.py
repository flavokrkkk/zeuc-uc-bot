import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from handlers import router
from config import load_bot_config, load_redis_config
from keyboards.commands import set_bot_commands


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    bot_config = load_bot_config()
    redis_config = load_redis_config()
    bot = Bot(token=bot_config.BOT_TOKEN)
    dp = Dispatcher()

    await set_bot_commands(bot)

    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())

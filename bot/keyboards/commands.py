from aiogram import Bot
from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from config import webapp_url


async def set_bot_commands(bot: Bot) -> None:
    menu_commands = {
        "/start": "Start",
        "/admin": "Admin panel",
    }
    commands = [
        BotCommand(
            command=command,
            description=description
        )
        for command, description in menu_commands.items()
    ]
    await bot.set_my_commands(commands)


def main_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text="Купить UC ♿️",
                web_app=WebAppInfo(url=webapp_url)
            )
        ],
        [InlineKeyboardButton(text="Цены 💵", callback_data="prices")],
        [
            InlineKeyboardButton(text="Поддержка 📞", callback_data="support"),
            InlineKeyboardButton(text="Отзывы📕", callback_data="reviews")
        ],
        [InlineKeyboardButton(text="пригласить друга", callback_data="invite")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
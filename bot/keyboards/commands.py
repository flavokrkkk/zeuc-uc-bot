from aiogram import Bot
from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from config.config import webapp_url


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


def admin_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="🇹🇷 Цены", callback_data="prices"),
            InlineKeyboardButton(text="🇹🇷 Коды", callback_data="uc_codes")
        ],
        [InlineKeyboardButton(text="🇹🇷 Рек-вы", callback_data="re")],
        [
            InlineKeyboardButton(text="🇹🇷 Статистика (Bot)", callback_data="bot_stats"),
            InlineKeyboardButton(text="🇹🇷 Статистика (UC)", callback_data="uc_stats")
        ],
        [InlineKeyboardButton(text="🇹🇷 Вкл | выкл", callback_data="handle_app")],
        [InlineKeyboardButton(text="🇹🇷 Черный список", callback_data="black_list")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_menu(is_admin: bool = False) -> InlineKeyboardMarkup:
    callback_data = "back_to_menu" if not is_admin else "back_to_admin_menu"
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="← Вернуться в меню", callback_data=callback_data)
        ]]
    )
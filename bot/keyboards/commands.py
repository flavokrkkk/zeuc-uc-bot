from aiogram import Bot
from aiogram.types import BotCommand, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from utils.config.config import REVIEWS_URL, SUPPORT_URL, WEB_APP_URL


async def set_bot_commands(bot: Bot) -> None:
    menu_commands = {
        "/start": "Start",
        # "/admin": "Admin panel",
    }
    commands = [
        BotCommand(command=command, description=description)
        for command, description in menu_commands.items()
    ]
    await bot.set_my_commands(commands)


def main_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Купить UC 🛒",web_app=WebAppInfo(url=WEB_APP_URL))
        ],
        [
            InlineKeyboardButton(text="Поддержка 📞", callback_data="support", url=SUPPORT_URL),
            InlineKeyboardButton(text="Отзывы📕", callback_data="reviews", url=REVIEWS_URL)
        ],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_menu_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="Коды", callback_data="uc_codes"),
            InlineKeyboardButton(text="Покупки", callback_data="purchases")
        ],
        [
            InlineKeyboardButton(text="Награды в колесе", callback_data="rewards")
        ],
        [
            InlineKeyboardButton(text="Статистика (Bot)", callback_data="bot_stats"),
            InlineKeyboardButton(text="Статистика (UC)", callback_data="uc_stats")
        ],
        [InlineKeyboardButton(text="Начислить бонусы", callback_data="add_bonuses")],
        [
            InlineKeyboardButton(text="Вкл | выкл", callback_data="off_or_on_store"),
            InlineKeyboardButton(text="Черный список", callback_data="black_list")
        ],
        [InlineKeyboardButton(text="История наград", callback_data="user_rewards")],
        [InlineKeyboardButton(text="Изменить кассу", callback_data="switch_payment_service")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_menu(is_admin: bool = False) -> InlineKeyboardMarkup:
    callback_data = "back_to_menu" if not is_admin else "back_to_admin_menu"
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(text="← Вернуться в меню", callback_data=callback_data)
        ]]
    )
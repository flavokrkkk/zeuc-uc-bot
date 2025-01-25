from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.decorators import add_back_to_menu_button


@add_back_to_menu_button(is_admin=True)
def get_stats_by_date_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
           [InlineKeyboardButton(text="Выбрать даты", callback_data="get_by_date")]
        ]
    )
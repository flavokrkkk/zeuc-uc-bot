from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from utils.decorators import add_back_to_menu_button


@add_back_to_menu_button(is_admin=True)
def get_stats_by_date_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
           [InlineKeyboardButton(text="Выбрать даты", callback_data="get_by_date")]
        ]
    )


@add_back_to_menu_button(is_admin=True)
def off_on_store_keyboard(store_is_on: bool) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Выключить магазин" if store_is_on else "Включить магазин", 
                callback_data="off_or_on_store_handle"
            )]
        ]
    )
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.decorators import add_back_to_menu_button


@add_back_to_menu_button(is_admin=True)
def all_uc_codes_keyboard(uc_codes: list[tuple[int, int]]) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for uc_amount, count in uc_codes:
        keyboard.button(
            text=f"{uc_amount} UC (x{count})", 
            callback_data=f"uc_codes_{uc_amount}"
        )

    keyboard.adjust(2)
    return keyboard.as_markup()


@add_back_to_menu_button(is_admin=True)
def uc_codes_options_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Добавить", callback_data=f"add_uc_codes"),
        InlineKeyboardButton(text="Удалить", callback_data=f"delete_uc_codes"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.decorators import add_back_to_menu_button


@add_back_to_menu_button(is_admin=True)
def all_uc_codes_keyboard(
    uc_codes: list[tuple[int, int]], 
    options_keyboard: bool = True, 
    view_count: bool = True
) -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()

    for uc_amount, count in uc_codes:
        keyboard.button(
            text=f"{uc_amount} UC (x{count})" if view_count else f"{uc_amount} UC",
            callback_data=f"uc_codes_{uc_amount}"
        )

    keyboard.adjust(2)
    keyboard = keyboard.as_markup()
    if options_keyboard:
        keyboard.inline_keyboard.append([
            InlineKeyboardButton(
                text="Добавить пак", 
                callback_data=f"add_uc_pack"
            )
        ])
    return keyboard


@add_back_to_menu_button(is_admin=True)
def uc_codes_options_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Добавить", callback_data=f"add_uc_codes")],
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete_uc_codes")],
        [InlineKeyboardButton(text="Изменить цену", callback_data=f"change_uc_code_price")],
        [InlineKeyboardButton(text="Изменить кол-во бонусы", callback_data="change_uc_code_point")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
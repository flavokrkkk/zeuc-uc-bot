from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.utils.decorators import add_back_to_menu_button


@add_back_to_menu_button(is_admin=True)
def purchase_keyboard(tg_id: int) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Изменить статус", callback_data="change_status"),
        InlineKeyboardButton(text="Связаться с покупателем", url=f"tg://user?id={tg_id}"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])



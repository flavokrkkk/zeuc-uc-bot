from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from utils.config.enums import PurchaseStatuses
from utils.decorators import add_back_to_menu_button


@add_back_to_menu_button(is_admin=True)
def purchase_menu_keyboard(tg_id: int) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Изменить статус", callback_data="change_status"),
        InlineKeyboardButton(text="Связаться с покупателем", url=f"tg://user?id={tg_id}"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@add_back_to_menu_button(is_admin=True)
def change_status_keyboard(status: str) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=PurchaseStatuses.IN_PROGRESS.value, callback_data="set_in_progress"),
        InlineKeyboardButton(text=PurchaseStatuses.COMPLETED.value, callback_data="set_completed"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
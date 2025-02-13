from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from database.models.models import Purchase
from utils.config.enums import PurchaseStatuses
from utils.decorators import add_back_to_menu_button


@add_back_to_menu_button(is_admin=True)
def purchase_menu_keyboard(username: int) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Изменить статус", callback_data="change_status"),
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@add_back_to_menu_button(is_admin=True)
def change_status_keyboard(status: str) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text=PurchaseStatuses.IN_PROGRESS.value, callback_data="set_in_progress"),
        InlineKeyboardButton(text=PurchaseStatuses.COMPLETED.value, callback_data="set_completed"),
        InlineKeyboardButton(text=PurchaseStatuses.CANCELED.value, callback_data="set_canceled")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@add_back_to_menu_button(is_admin=True)
def search_purchase_methods_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="По номеру заказа", callback_data="search_by_order_id"),
        InlineKeyboardButton(text="По дате", callback_data="search_by_date")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@add_back_to_menu_button(is_admin=True)
def purchases_pagination_keyboard(purchases: list[Purchase], pages: int, page: int) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=f"{purchase.payment_id}",
                callback_data=f"purchase_{purchase.payment_id}"
            )
        ] for purchase in purchases
    ]

    if purchases:
        pagination = []
        if page > 1:
            pagination.append(
                InlineKeyboardButton(
                    text="←",
                    callback_data=f"purchases_page_{page - 1}"
                )
            )
        if page < pages:
            pagination.append(
                InlineKeyboardButton(
                    text="→",
                    callback_data=f"purchases_page_{page + 1}"
                )
            )

        buttons.append(pagination)
        return InlineKeyboardMarkup(inline_keyboard=buttons)
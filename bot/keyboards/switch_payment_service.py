from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bot.utils.config.enums import BuyServices
from bot.utils.decorators import add_back_to_menu_button


@add_back_to_menu_button(is_admin=True)
def switch_payment_service_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=service.value, callback_data=service.value)]
            for service in BuyServices
        ]
    )
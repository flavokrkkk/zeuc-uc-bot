
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def add_back_to_menu_button(is_admin: bool = False):
    def decorator(func):
        def wrapper(*args, **kwargs) -> InlineKeyboardBuilder | InlineKeyboardMarkup:
            button_data = {
                "text": "← Вернуться в меню", 
                "callback_data": "back_to_menu" if not is_admin else "back_to_admin_menu"
            }
            keyboard = func(*args, **kwargs)
            if isinstance(keyboard, InlineKeyboardBuilder):
                keyboard.button(**button_data)
            if isinstance(keyboard, InlineKeyboardMarkup):
                keyboard.inline_keyboard.append([InlineKeyboardButton(**button_data)])
            return keyboard
        return wrapper
    return decorator
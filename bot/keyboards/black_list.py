from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from database.models.models import User
from utils.decorators import add_back_to_menu_button


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models.models import User
from utils.decorators import add_back_to_menu_button


@add_back_to_menu_button(is_admin=True)
def black_list_pagination(users: list[User], pages: int, page: int) -> InlineKeyboardMarkup:
    users_buttons = [
        [
            InlineKeyboardButton(
                text=f"{user.username}",
                callback_data=f"black_list_user_{user.tg_id}"
            )
        ] for user in users
    ]
    
    users_buttons.extend([
        [
            InlineKeyboardButton(
                text="Добавить", 
                callback_data="add_to_black_list"
            ),
            InlineKeyboardButton(
                text="Удалить",
                callback_data="remove_from_black_list"
            )
        ]
    ])
    
    pagination = []
    if page > 1:
        pagination.append(
            InlineKeyboardButton(
                text="←",
                callback_data=f"black_list_page_{page - 1}"
            )
        )
    if page < pages:
        pagination.append(
            InlineKeyboardButton(
                text="→",
                callback_data=f"black_list_page_{page + 1}"
            )
        )

        users_buttons.append(pagination)
    return InlineKeyboardMarkup(inline_keyboard=users_buttons)

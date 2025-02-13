from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models.models import UserRewards
from utils.decorators import add_back_to_menu_button


@add_back_to_menu_button(is_admin=True)
def user_rewards_options_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="По дате", callback_data=f"check_by_date"),
        InlineKeyboardButton(text="По юзернейму", callback_data=f"check_by_username")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@add_back_to_menu_button(is_admin=True)
def user_rewards_keyboard(user_rewards: list[UserRewards], pages: int, page: int) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(
            text=(
                f"{user_reward.reward.uc_amount} UC" 
                if user_reward.reward.reward_type == "uc_code"
                else f"{user_reward.reward.discount.value} при покупке от {user_reward.reward.discount.min_payment_value}"
            ),
            callback_data=f"check_reward_{user_reward.reward_id}")
        for user_reward in user_rewards
    ]

    if pages:
        pagination = []
        if page > 1:
            pagination.append(
                InlineKeyboardButton(
                    text="←",
                    callback_data=f"user_rewards_page_{page - 1}"
                )
            )
        if page < pages:
            pagination.append(
                InlineKeyboardButton(
                    text="→",
                    callback_data=f"user_rewards_page_{page + 1}"
                )
            )

        buttons.append(pagination)  
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@add_back_to_menu_button(is_admin=True)
def user_reward_edit_keyboard(username: str) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Изменить статус", callback_data="change_status"),
        InlineKeyboardButton(text="Связаться с покупателем", callback_data=f"t.me//{username}")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@add_back_to_menu_button(is_admin=True)
def user_reward_statuses_keyboard(is_paid: bool):
    buttons = [
        InlineKeyboardButton(text="Получен", callback_data="is_paid"),
        InlineKeyboardButton(text="Не получен", callback_data="not_is_paid")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
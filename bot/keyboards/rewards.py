from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.models.models import Reward
from utils.decorators import add_back_to_menu_button


@add_back_to_menu_button(is_admin=True)
def rewards_keyboard(rewards: list[Reward]) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text=f"{reward.uc_amount} UC", callback_data=f"reward_{reward.reward_id}")]
        if reward.reward_type == "uc_code"
        else 
        [
            InlineKeyboardButton(
                text=f"{reward.discount.value} при покупке от {reward.discount.min_payment_value}", 
                callback_data=f"reward_{reward.reward_id}"
            )
        ]
        for reward in rewards
    ]
    buttons.append([InlineKeyboardButton(text="Добавить", callback_data=f"add_reward")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


@add_back_to_menu_button(is_admin=True)
def reward_options_keyboard(reward: Reward) -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="Удалить", callback_data=f"delete_reward_{reward.reward_id}")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])


@add_back_to_menu_button(is_admin=True)
def choose_reward_type_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        InlineKeyboardButton(text="UC Pack", callback_data="uc_codes"),
        InlineKeyboardButton(text="Скидка", callback_data="discount")
    ]
    return InlineKeyboardMarkup(inline_keyboard=[buttons])
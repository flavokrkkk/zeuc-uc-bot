from datetime import datetime
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from utils.formats import format_user_reward
from database.models.models import Discount, UserRewards
from database.db_main import Database
from keyboards.commands import back_to_menu
from keyboards.user_rewards import user_reward_edit_keyboard, user_reward_statuses_keyboard, user_rewards_keyboard, user_rewards_options_keyboard
from states.menu import AdminMenuStates
from states.user_rewards import UserRewardsStates


router = Router()


@router.callback_query(AdminMenuStates.main, F.data == "user_rewards")
async def user_rewards_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserRewardsStates.choose_option)
    await callback_query.message.edit_text(
        text="Выберите способ поиска наград",
        reply_markup=user_rewards_options_keyboard()
    )


@router.callback_query(UserRewardsStates.choose_option, F.data == "check_by_username")
async def user_rewards_callback(callback_query: CallbackQuery, state: FSMContext, database: Database):
    await state.set_state(UserRewardsStates.input_username)
    await callback_query.message.edit_text(
        text="Введите юзернейм пользователя",
        reply_markup=back_to_menu(is_admin=True)
    )


@router.message(UserRewardsStates.input_username)
async def user_rewards_input_username(message: Message, state: FSMContext, database: Database):
    user = await database.users.get_by_username(message.text)
    if not user:
        return await message.answer(
            text="Пользователь не найден",
            reply_markup=back_to_menu(is_admin=True)
        )
    else:
        user_rewards = await database.user_rewards.get_user_rewards(user.tg_id, 0)
        if not user_rewards:
            return await message.answer(
                text="У пользователя нет наград",
                reply_markup=back_to_menu(is_admin=True)
            )
    
    await state.set_state(UserRewardsStates.check_by_username)
    await state.update_data(tg_id=user.tg_id)
    await message.answer(
        text="Список всех наград пользователя",
        reply_markup=user_rewards_keyboard(user_rewards, 0, 0)
    )


@router.callback_query(UserRewardsStates.choose_option, F.data == "check_by_date")
async def user_rewards_callback(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(UserRewardsStates.input_date)
    await callback_query.message.edit_text(
        text="Отправьте дату в формате ДД.ММ.ГГГГ - ДД.ММ.ГГГГ",
        reply_markup=back_to_menu(is_admin=True)
    )


@router.message(UserRewardsStates.input_date)
async def user_rewards_input_date(message: Message, state: FSMContext, database: Database):
    try:
        start_date, end_date = map(
            lambda x: int(
                datetime.strptime(x, "%d.%m.%Y").timestamp() * 1000
            ),
            message.text.split(" - ")
        )

        user_rewards = await database.user_rewards.get_user_rewards_by_date(start_date, end_date, 0)
        if not user_rewards:
            await message.answer(
                text="Нет данных",
                reply_markup=back_to_menu(is_admin=True)
            )
        else:
            await state.set_state(UserRewardsStates.check_by_date)
            await state.update_data(start_date=start_date, end_date=end_date)
            await message.answer(
                text="Список всех наград пользователя",
                reply_markup=user_rewards_keyboard(user_rewards, 0, 0)
            )
    except Exception as e:
        await message.answer(
            text="Неверный формат даты",
            reply_markup=back_to_menu(is_admin=True)
        )


@router.callback_query(UserRewardsStates.check_by_date, F.data.startswith("user_rewards_page_"))
async def check_user_rewards_pagination(callback: CallbackQuery, state: FSMContext, database: Database):
    page = int(callback.data.split("_")[-1])
    data = await state.get_data() or {}
    start_date, end_date = data.get("start_date"), data.get("end_date")

    user_rewards = await database.user_rewards.get_user_rewards_by_date(start_date, end_date, page)
    pages = await database.user_rewards.get_user_rewards_by_date_pages(start_date, end_date)

    await callback.message.edit_text(
        text="Список всех наград пользователя",
        reply_markup=user_rewards_keyboard(user_rewards, pages, page)
    )


@router.callback_query(UserRewardsStates.check_by_username, F.data.startswith("user_rewards_page_"))
async def check_user_rewards_pagination(callback: CallbackQuery, state: FSMContext, database: Database):
    page = int(callback.data.split("_")[-1])
    tg_id = (await state.get_data() or {}).get("tg_id")

    user_rewards = await database.user_rewards.get_user_rewards(tg_id, page)
    pages = await database.user_rewards.get_user_rewards_pages(tg_id)

    await callback.message.edit_text(
        text="Список всех наград пользователя",
        reply_markup=user_rewards_keyboard(user_rewards, pages, page)
    )


@router.callback_query(F.data.startswith("check_reward_"))
async def check_reward(callback: CallbackQuery, state: FSMContext, database: Database):
    user_reward_id = int(callback.data.split("_")[-1])
    user_reward: UserRewards = await database.user_rewards.get_item(user_reward_id)
    
    await state.set_state(UserRewardsStates.check_page)
    await state.update_data(user_reward_id=user_reward_id)

    await callback.message.edit_text(
        text=await format_user_reward(user_reward, database),
        reply_markup=user_reward_edit_keyboard(user_reward.user.username)
    )


@router.callback_query(UserRewardsStates.check_page)
async def choose_status(callback: CallbackQuery, state: FSMContext, database: Database):
    user_reward_id = int((await state.get_data() or {}).get("user_reward_id"))
    user_reward: UserRewards = await database.user_rewards.get_item(user_reward_id)
    
    await state.set_state(UserRewardsStates.change_status)
    await callback.message.edit_text(
        text="Выберите статус",
        reply_markup=user_reward_statuses_keyboard(user_reward.is_used)
    )


@router.callback_query(UserRewardsStates.change_status)
async def change_status(callback: CallbackQuery, state: FSMContext, database: Database):
    user_reward_id = int((await state.get_data() or {}).get("user_reward_id"))
    user_reward: UserRewards = await database.user_rewards.get_item(user_reward_id)

    await database.user_rewards.update_item(
        UserRewards.id,
        user_reward_id, 
        is_used=callback.data == "is_paid"
    )
    await state.set_state(UserRewardsStates.check_page)
    await callback.message.edit_text(
        text=await format_user_reward(user_reward, database),
        reply_markup=user_reward_edit_keyboard(user_reward.user.username)
    )
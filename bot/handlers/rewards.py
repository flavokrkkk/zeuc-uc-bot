from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.menu import AdminMenuStates
from database.models.models import Discount, Reward
from keyboards.commands import back_to_menu
from keyboards.uc_codes import all_uc_codes_keyboard
from database.db_main import Database
from keyboards.rewards import choose_reward_type_keyboard, reward_options_keyboard, rewards_keyboard
from states.rewards import AddDiscountReward, AddUCPackReward, RewardsStates


router = Router()


@router.callback_query(F.data == "rewards", AdminMenuStates.main)
async def rewards(callback: CallbackQuery, state: FSMContext, database: Database):
    rewards = await database.rewards.get_all_items()
    await state.set_state(RewardsStates.choose)
    await callback.message.edit_text(
        text="Выберите награду, которую хотите удалить",
        reply_markup=rewards_keyboard(rewards)
    )



@router.callback_query(F.data.startswith("reward_"))
async def reward(callback: CallbackQuery, state: FSMContext, database: Database):
    reward_id = int(callback.data.split("_")[-1])
    reward: Reward = await database.rewards.get_item(reward_id)

    if not reward:
        await callback.message.edit_text(
            text="Награда не найдена",
            reply_markup=back_to_menu(is_admin=True)
        )
    else:
        await state.update_data(reward_id=reward_id)
        await state.set_state(RewardsStates.check_reward)

        await callback.message.edit_text(
            text=f"Выберите опцию для {reward.reward_type} награды",
            reply_markup=reward_options_keyboard(reward)
        )


@router.callback_query(F.data.startswith("delete_reward_"))
async def delete_reward(callback: CallbackQuery, state: FSMContext, database: Database):
    reward_id = int(callback.data.split("_")[-1])
    
    reward = await database.rewards.get_item(reward_id)
    if not reward:
        await callback.message.edit_text(
            text="Награда не найдена",
            reply_markup=back_to_menu(is_admin=True)
        )
    else:
        await database.rewards.delete_item(reward)
        await callback.message.edit_text(
            text="Награда успешно удалена",
            reply_markup=back_to_menu(is_admin=True)
        )


@router.callback_query(F.data == "add_reward", RewardsStates.choose)
async def add_reward(callback: CallbackQuery, state: FSMContext):
    await state.set_state(RewardsStates.choose_add_reward_type)
    await callback.message.edit_text(
        text="Выберите тип награды",
        reply_markup=choose_reward_type_keyboard()
    )


@router.callback_query(F.data == "uc_codes", RewardsStates.choose_add_reward_type)
async def add_reward_uc_pack(callback: CallbackQuery, state: FSMContext, database: Database):
    uc_codes = await database.uc_codes.group_by_amount()
    await state.set_state(AddUCPackReward.choose_uc_pack)
    await state.update_data(reward_type="uc_code")
    await callback.message.edit_text(
        text="Выберите пак",
        reply_markup=all_uc_codes_keyboard(uc_codes, options_keyboard=False, view_count=False)
    )


@router.callback_query(F.data.startswith("uc_codes_"), AddUCPackReward.choose_uc_pack)
async def succes_add_uc_pack_reward(callback: CallbackQuery, state: FSMContext, database: Database):
    uc_amount = int(callback.data.split("_")[-1])
    await database.rewards.add_item(uc_amount=uc_amount, **(await state.get_data()))
    await state.set_state(AddUCPackReward.success)
    await callback.message.edit_text(
        text="Награда успешно добавлена",
        reply_markup=back_to_menu(is_admin=True)
    )


@router.callback_query(F.data == "discount", RewardsStates.choose_add_reward_type)
async def add_discount_reward(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddDiscountReward.input_discount_value)
    await callback.message.edit_text(
        text="Введите скидку",
        reply_markup=back_to_menu(is_admin=True)
    )


@router.message(F.text, AddDiscountReward.input_discount_value)
async def add_discount_reward_value(message: Message, state: FSMContext, database: Database):
    try:
        value = int(message.text)
        if value <= 0:
            await message.answer(
                text="Неверная скидка",
                reply_markup=back_to_menu(is_admin=True)
            )
        else:
            await state.update_data(value=value)
            await state.set_state(AddDiscountReward.input_min_payment_value)
            await message.answer(
                text="Введите минимальную сумму покупки",
                reply_markup=back_to_menu(is_admin=True)
            )
    except Exception as e:
        await message.answer(
            text="Неверная скидка",
            reply_markup=back_to_menu(is_admin=True)
        )


@router.message(F.text, AddDiscountReward.input_min_payment_value)
async def add_discount_reward_min_payment(message: Message, state: FSMContext, database: Database):
    try:
        min_payment_value = int(message.text)
        if min_payment_value <= 0:
            await message.answer(
                text="Неверная сумма покупки",
                reply_markup=back_to_menu(is_admin=True)
            )
        else:
            discount: Discount = await database.discounts.add_item(
                min_payment_value=min_payment_value, 
                **(await state.get_data())
            )
            await database.rewards.add_item(discount_id=discount.discount_id, reward_type="discount")
            await state.set_state(AddDiscountReward.success)
            await message.answer(
                text="Награда успешно добавлена",
                reply_markup=back_to_menu(is_admin=True)
            )
    except Exception as e:
        await message.answer(
            text="Неверная сумма покупки",
            reply_markup=back_to_menu(is_admin=True)
        )
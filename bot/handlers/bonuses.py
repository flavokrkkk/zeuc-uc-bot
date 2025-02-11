from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.menu import AdminMenuStates
from database.db_main import Database
from states.bonuses import AddBonusesStates
from keyboards.commands import back_to_menu


router = Router()


@router.callback_query(F.data == "add_bonuses", AdminMenuStates.main)
async def add_bonuses(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddBonusesStates.input_username)
    await callback.message.edit_text(
        text="Введите юзернейм пользователя, которому хотите начислить бонусы",
        reply_markup=back_to_menu(is_admin=True)
    )


@router.message(F.text, AddBonusesStates.input_username)
async def input_username(message: Message, state: FSMContext, database: Database):
    user = await database.users.get_by_username(message.text)
    if not user:
        await message.answer(
            text="Пользователь с таким юзернеймом не найден, попробуйте еще раз",
            reply_markup=back_to_menu(is_admin=True)
        )
    else:
        await state.update_data(username=message.text)
        await state.set_state(AddBonusesStates.input_amount)
        await message.answer(
            text="Введите количество бонусов, которое хотите начислить",
            reply_markup=back_to_menu(is_admin=True)
        )


@router.message(F.text, AddBonusesStates.input_amount)
async def input_quantity(message: Message, state: FSMContext, database: Database):
    try:
        amount = int(message.text)
        if amount < 0:
            raise ValueError
    except ValueError:
        await message.answer(
            text="Количество должно быть числом, попробуйте еще раз",
            reply_markup=back_to_menu(is_admin=True)
        )
    else:
        data = await state.get_data()
        await database.users.add_bonuses(data.get("username"), amount)
        await state.set_state(AddBonusesStates.success)
        await message.answer(
            text=f"Бонусы успешно начислены пользователю {data['username']}",
            reply_markup=back_to_menu(is_admin=True)
        )
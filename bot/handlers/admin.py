from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.commands import admin_menu_keyboard, back_to_menu
from states.uc_codes import UCCodesStates
from keyboards.admin import all_uc_codes_keyboard, uc_codes_options_keyboard
from database.db_main import Database


router = Router()


@router.callback_query(F.data == "back_to_admin_menu")
async def back_to_admin_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        text="Вы находитесь в админ меню",
        reply_markup=admin_menu_keyboard()
    )


@router.callback_query(F.data == "uc_codes")
async def get_uc_codes(callback: CallbackQuery, state: FSMContext, database: Database):
    message_text = "Выберите позицию для удаления или добавления"
    await state.set_state(UCCodesStates.main)

    codes = await database.uc_codes.group_by_amount()
    await callback.message.edit_text(
        text=message_text,
        reply_markup=all_uc_codes_keyboard(codes)
    )


@router.callback_query(F.data.startswith("uc_codes"), UCCodesStates.main)
async def uc_codes_by_value(callback: CallbackQuery, state: FSMContext):
    uc_amount = int(callback.data.split("_")[-1])
    message_text = "Выберите желаемую опцию"
    
    await state.set_state(UCCodesStates.option)
    await state.update_data(uc_amount=uc_amount)

    await callback.message.edit_text(
        text=message_text,
        reply_markup=uc_codes_options_keyboard()
    )


@router.callback_query(F.data.startswith(""), UCCodesStates.option)
async def delete_codes(callback: CallbackQuery, state: FSMContext, database: Database):
    ucinitial = (await state.get_data() or {}).get("uc_amount")
    message_text = f"Введите количество кодов, которые хотите удалить. Вы выбрали {ucinitial} UC"

    await state.set_state(UCCodesStates.delete_code)
    await callback.message.edit_text(
        text=message_text,
        reply_markup=uc_codes_options_keyboard()
    )


@router.message(F.text, UCCodesStates.delete_code)
async def delete_codes_quantity(message: Message, state: FSMContext, database: Database):
    quantity = int(message.text)
    uc_amount = (await state.get_data()).get("uc_amount")

    uc_codes_quantity = await database.uc_codes.get_by_amount(uc_amount=uc_amount)
    if quantity > uc_codes_quantity:
        message_text = f"Вы пытаетесь удалить больше кодов, чем есть в базе. Выберите количество удаляемых кодов"
        await message.answer(
            text=message_text,
            reply_markup=back_to_menu(is_admin=True)
        )
    await database.uc_codes.delete_codes_by_value(uc_amount=uc_amount, quantity=quantity)
    
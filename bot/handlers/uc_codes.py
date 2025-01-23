from io import BytesIO
from tempfile import NamedTemporaryFile
from typing import BinaryIO
from aiogram import F, Bot, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, FSInputFile, Message

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


@router.callback_query(F.data == "delete_uc_codes", UCCodesStates.option)
async def delete_codes(callback: CallbackQuery, state: FSMContext, database: Database):
    ucinitial = (await state.get_data() or {}).get("uc_amount")
    message_text = f"Введите количество кодов, которые хотите удалить. Вы выбрали {ucinitial} UC"

    await state.set_state(UCCodesStates.delete_code)
    await callback.message.edit_text(
        text=message_text, 
        reply_markup=back_to_menu(is_admin=True)
    )


@router.message(F.text, UCCodesStates.delete_code)
async def delete_codes_quantity(message: Message, state: FSMContext, database: Database):
    quantity = int(message.text)
    uc_amount = (await state.get_data()).get("uc_amount")

    uc_codes_quantity = await database.uc_codes.get_count_by_amount(uc_amount=uc_amount)
    if quantity > uc_codes_quantity:
        message_text = f"Вы пытаетесь удалить больше кодов, чем есть в базе. Выберите количество удаляемых кодов"
        await message.answer(
            text=message_text,
            reply_markup=back_to_menu(is_admin=True)
        )
    else:
        deleted_codes = await database.uc_codes.delete_codes_by_value(
            uc_amount=uc_amount, 
            quantity=quantity
        )
        deleted_codes = await database.uc_codes.delete_codes_by_value(
            uc_amount=uc_amount, 
            quantity=quantity
        )

        if not deleted_codes:
            await message.answer("Нет кодов для удаления.")
            return

        file_content = "\n".join(deleted_codes).encode("utf-8")
        deleted_uc_codes_file = BufferedInputFile(
            file_content, 
            filename="{uc_amount} UC.txt".format(uc_amount=uc_amount)
        )

        await state.set_state(UCCodesStates.main)
        await message.answer_document(
            document=deleted_uc_codes_file,
            caption="Список удалённых кодов",
            reply_markup=back_to_menu(is_admin=True),
        )
            

@router.callback_query(F.data == "add_uc_codes", UCCodesStates.option)
async def add_uc_codes(callback: CallbackQuery, state: FSMContext):
    message_text = "Отправьте файл с uc кодами"

    await state.set_state(UCCodesStates.upload_codes)
    await callback.message.edit_text(
        text=message_text,
        reply_markup=back_to_menu(is_admin=True)
    )


@router.message(F.document, UCCodesStates.upload_codes)
async def upload_new_codes(
    message: Message, 
    state: FSMContext, 
    database: Database, 
    bot: Bot
):
    await state.set_state(UCCodesStates.succes)
    
    file_data = BytesIO()
    file = await bot.download(message.document.file_id, file_data)
    
    new_uc_codes = [uc_code.decode("utf-8") for uc_code in file.readlines()]
    uc_amount = int((await state.get_data() or {}).get("uc_amount"))
    await database.uc_codes.add_new_codes(new_uc_codes, uc_amount)
    
    message_text = f"Коды успешно добавлены. Вы добавили {len(new_uc_codes)} кодов"
    await message.answer(
        text=message_text,
        reply_markup=back_to_menu(is_admin=True)
    )

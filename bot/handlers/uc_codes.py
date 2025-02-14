from io import BytesIO
from aiogram import F, Bot, Router      
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, FSInputFile, Message
from sqlalchemy.exc import IntegrityError

from states.menu import AdminMenuStates
from keyboards.commands import back_to_menu
from states.uc_codes import AddNewPackStates, UCCodesStates
from keyboards.uc_codes import all_uc_codes_keyboard, uc_codes_options_keyboard
from database.db_main import Database


router = Router()


@router.callback_query(F.data == "uc_codes", AdminMenuStates.main)
async def get_uc_codes(callback: CallbackQuery, state: FSMContext, database: Database):
    message_text = "Выберите позицию для удаления или добавления"
    await state.set_state(UCCodesStates.main)

    codes = await database.uc_codes.group_by_amount()
    await callback.message.edit_text(
        text=message_text,
        reply_markup=all_uc_codes_keyboard(codes)
    )


@router.callback_query(F.data.startswith("uc_codes"), UCCodesStates.main)
async def uc_codes_by_value(callback: CallbackQuery, state: FSMContext, database: Database):
    uc_amount = int(callback.data.split("_")[-1])
    price = await database.uc_codes.get_price_by_amount(uc_amount)
    message_text = (
        f"Цена: {price.price}\n"
        f"Количество бонусов: {price.point}\n"
        f"UC Pack: {price.uc_amount}"
    )
    
    await state.set_state(UCCodesStates.option)
    await state.update_data(uc_amount=uc_amount)

    await callback.message.edit_text(
        text=message_text,
        reply_markup=uc_codes_options_keyboard()
    )


@router.callback_query(F.data == "change_uc_code_point", UCCodesStates.option)
async def input_uc_code_point(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UCCodesStates.change_uc_code_point)
    await callback.message.edit_text(text="Введите новое количество бонусов")


@router.message(F.text, UCCodesStates.change_uc_code_point)
async def update_uc_pack_point(message: Message, state: FSMContext, database: Database):
    try:
        point = int(message.text)
        if point <= 0:
            raise
        else:
            uc_amount = (await state.get_data() or {}).get("uc_amount")
            await database.uc_codes.change_point(uc_amount, point)
            await state.set_state(UCCodesStates.success)
            await message.answer(
                text="Количество бонусов успешно изменено",
                reply_markup=back_to_menu(is_admin=True)
            )
    except:
        await message.answer(
            text="Неверное количество бонусов",
            reply_markup=back_to_menu(is_admin=True)
        )


@router.callback_query(F.data == "delete_uc_codes", UCCodesStates.option)
async def delete_codes(callback: CallbackQuery, state: FSMContext, database: Database):
    uc_amount = (await state.get_data() or {}).get("uc_amount")
    message_text = f"Введите количество кодов, которые хотите удалить. Вы выбрали {uc_amount} UC"

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
            caption="Список удалённых кодов"
        )
            

@router.callback_query(F.data == "add_uc_codes", UCCodesStates.option)
async def add_uc_codes(callback: CallbackQuery, state: FSMContext):
    message_text = "Отправьте файл с uc кодами или сообщение с кодами, где каждый код с новой строки"

    await state.set_state(UCCodesStates.upload_codes)
    await callback.message.edit_text(
        text=message_text,
        reply_markup=back_to_menu(is_admin=True)
    )


@router.message(F.text, UCCodesStates.upload_codes)
async def upload_new_codes_text(message: Message, state: FSMContext, database: Database):
    try:
        new_uc_codes = message.text.split("\n")
        uc_amount = (await state.get_data() or {}).get("uc_amount")
        await database.uc_codes.add_new_codes(new_uc_codes, uc_amount)
        
        message_text = f"Коды успешно добавлены. Вы добавили {len(new_uc_codes)} кодов"
        await message.answer(
            text=message_text
        )
    except IntegrityError:
        await message.answer(
            text="Код(-ы) уже добавлен(-ы)",
            reply_markup=back_to_menu(is_admin=True)
        )
    except:
        await message.answer(
            text="Неверный формат",
            reply_markup=back_to_menu(is_admin=True)
        )

@router.message(F.document, UCCodesStates.upload_codes)
async def upload_new_codes_file(
    message: Message, 
    state: FSMContext, 
    database: Database, 
    bot: Bot
):
    try:
        await state.set_state(UCCodesStates.success)
        
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
    except IntegrityError:
        await message.answer(
            text="Код(-ы) уже добавлен(-ы)",
            reply_markup=back_to_menu(is_admin=True)
        )
    except:
        await message.answer(
            text="Неверный формат файла",
            reply_markup=back_to_menu(is_admin=True)
        )


@router.callback_query(F.data == "add_uc_pack", UCCodesStates.main)
async def add_uc_pack_amount(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AddNewPackStates.add_uc_pack_amount)
    await callback.message.edit_text(text="Введите количесто UC в паке")


@router.message(F.text, AddNewPackStates.add_uc_pack_amount)
async def add_uc_pack_price(message: Message, state: FSMContext):
    try:
        uc_amount = int(message.text)
        if uc_amount <= 0:
            raise
        else:
            await state.update_data(uc_amount=uc_amount)
            await state.set_state(AddNewPackStates.add_uc_pack_price)
            await message.answer(text="Введите стоимость пака")
    except:
        await message.answer(
            text="Неверное количество UC кодов",
            reply_markup=back_to_menu(is_admin=True)
        )
    

@router.message(F.text, AddNewPackStates.add_uc_pack_price)
async def add_uc_pack_price(message: Message, state: FSMContext):
    try:
        price = int(message.text)
        if price <= 0:
            raise
        else:
            await state.update_data(price_per_uc=price)
            await state.set_state(AddNewPackStates.add_uc_pack_point)
            await message.answer(text="Введите количество бонусов за покупку")
    except:
        await message.answer(
            text="Неверная стоимость пака",
            reply_markup=back_to_menu(is_admin=True)
        )


@router.message(F.text, AddNewPackStates.add_uc_pack_point)
async def add_uc_pack_point(message: Message, state: FSMContext):
    try:
        point = int(message.text)
        if point <= 0:
            raise
        else:
            await state.update_data(point=point)
            await state.set_state(AddNewPackStates.add_uc_pack_file)
            message_text = "Отправьте файл с uc кодами или сообщение с кодами, где каждый код с новой строки"
            await message.answer(text=message_text)
    except:
        await message.answer(
            text="Неверное количество бонусов",
            reply_markup=back_to_menu(is_admin=True)
        )


@router.message(F.document, AddNewPackStates.add_uc_pack_file)
async def upload_new_codes(
    message: Message, 
    state: FSMContext, 
    database: Database, 
    bot: Bot
):
    try:
        await state.set_state(UCCodesStates.success)
        
        file_data = BytesIO()
        file = await bot.download(message.document.file_id, file_data)
        
        new_uc_codes = [uc_code.decode("utf-8") for uc_code in file.readlines()]
        await database.uc_codes.add_uc_pack(new_uc_codes, **(await state.get_data()))
        
        message_text = f"Коды успешно добавлены. Вы добавили {len(new_uc_codes)} кодов"
        await message.answer(
            text=message_text,
            reply_markup=back_to_menu(is_admin=True)
        )
    except IntegrityError:
        await message.answer(
            text="Код(-ы) уже добавлен(-ы)",
            reply_markup=back_to_menu(is_admin=True)
        )
    except:
        await message.answer(
            text="Неверный формат файла",
            reply_markup=back_to_menu(is_admin=True)
        )


@router.message(F.text, AddNewPackStates.add_uc_pack_file)
async def upload_new_codes_text(message: Message, state: FSMContext, database: Database):
    try:
        new_uc_codes = message.text.split("\n")
        await database.uc_codes.add_uc_pack(new_uc_codes, **(await state.get_data()))
        
        message_text = f"Коды успешно добавлены. Вы добавили {len(new_uc_codes)} кодов"
        await message.answer(
            text=message_text,
            reply_markup=back_to_menu(is_admin=True)
        )
    except IntegrityError:
        await message.answer(
            text="Код(-ы) уже добавлен(-ы)",
            reply_markup=back_to_menu(is_admin=True)
        )
    except Exception as e:
        await message.answer(
            text="Неверный формат",
            reply_markup=back_to_menu(is_admin=True)
        )

@router.callback_query(F.data == "change_uc_code_price", UCCodesStates.option)
async def change_uc_code_price(callback: CallbackQuery, state: FSMContext):
    await state.set_state(UCCodesStates.change_price)
    await callback.message.edit_text(text="Введите новую цену")
    

@router.message(F.text, UCCodesStates.change_price)
async def change_uc_code_price(message: Message, state: FSMContext, database: Database):
    try:
        price = int(message.text)
        if price <= 0:
            raise
        else:
            uc_amount = (await state.get_data() or {}).get("uc_amount")
            await database.uc_codes.change_price(uc_amount, price)
            await state.set_state(UCCodesStates.success)
            await message.answer(
                text=f"Цена успешно изменена. Новая цена {price} для {uc_amount} UC",
                reply_markup=back_to_menu(is_admin=True)
            )
    except:
        await message.answer(
            text="Неверная цена",
            reply_markup=back_to_menu(is_admin=True)
        )

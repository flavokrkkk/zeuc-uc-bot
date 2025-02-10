from datetime import datetime
import json
from textwrap import dedent
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from database.models.models import Purchase
from utils.config.enums import PurchaseStatuses
from database.models.models import User
from keyboards.commands import back_to_menu
from keyboards.purchases import purchase_menu_keyboard, change_status_keyboard, purchases_pagination_keyboard, search_purchase_methods_keyboard
from states.purchases import PurchasesStates
from database.db_main import Database


router = Router()

from datetime import datetime

def format_purchase_data(purchase: Purchase, data: dict[str, str]) -> str:
    us_packs_info = []
    for uc_pack in data['uc_packs']:
        errors = "\n" + "\n".join([
            "{uc_code} → {message}".format(uc_code=err['uc_code'], message=err['message'])
            for err in uc_pack['errors']
        ]) if uc_pack['errors'] else "Нет ошибок"

        pack_info = (
            f"<b>Сумма</b>: {uc_pack['total_sum']} ₽\n"
            f"<b>Количество UC</b>: {uc_pack['uc_amount']} UC x {uc_pack['quantity']}\n"
            f"<b>Количество активированных кодов</b>: {uc_pack['activated_codes']}\n"
            f"<b>Неуспешные Activation IDs</b>: {uc_pack.get('error_activation_ids')}\n"
            f"<b>Ошибки активации (Код → Ошибка)</b>: {errors}"
        ).strip()

        us_packs_info.append(pack_info)

    message_text = (
        f"<b>Заказ</b>: {purchase.payment_id}\n"
        f"<b>Дата покупки</b>: {datetime.fromtimestamp(purchase.created_at / 1000).strftime('%d.%m.%Y %H:%M:%S')}\n"
        f"<b>Игрок</b>: {purchase.player_id}\n"
        f"<b>Сумма UC</b>: {purchase.uc_sum} ₽\n"
        f"<b>Сумма заказа</b>: {purchase.price} ₽\n"
        f"<b>Метод оплаты</b>: {purchase.payment_method}\n"
        f"<b>Статус</b>: {purchase.status}\n\n"
        f"<b>Информация по UC-пакетам:</b>\n\n" + "\n\n".join(us_packs_info)
    ).strip()

    return message_text



@router.callback_query(F.data == "purchases")
async def purchases(callback: CallbackQuery, state: FSMContext, database: Database):
    await state.set_state(PurchasesStates.choose_method)
    await callback.message.edit_text(
        text="Выберите метод поиска",
        reply_markup=search_purchase_methods_keyboard()
    )


@router.callback_query(F.data == "search_by_date", PurchasesStates.choose_method)
async def search_by_date(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PurchasesStates.input_date)
    await callback.message.edit_text(
        text="Отправьте дату в формате ДД.ММ.ГГГГ - ДД.ММ.ГГГГ",
        reply_markup=back_to_menu(is_admin=True)
    )


@router.message(F.text, PurchasesStates.input_date)
async def input_date(message: Message, state: FSMContext, database: Database):
    print(message.text)
    try:
        start_data, end_date = map(
            lambda x: int(
                datetime.strptime(x, "%d.%m.%Y").timestamp() * 1000
            ),
            message.text.split(" - ")
        )
        purchases = await database.purchases.get_by_date(start_data, end_date, 0)
        if not purchases:
            await message.answer(
                text="Нет данных",
                reply_markup=back_to_menu(is_admin=True)
            )
        else:
            pages = await database.purchases.get_pages_by_date(start_data, end_date)
            message_text = "Выберите заказ для просмотра подробной информации"

            await state.set_state(PurchasesStates.check_order)
            await state.update_data(start_date=start_data, end_date=end_date)
            await message.answer(
                text=message_text if message_text else "Нет данных",
                reply_markup=purchases_pagination_keyboard(purchases, pages, 0)
            )
    except Exception as e:
        await message.answer(
            text="Неверный формат даты",
            reply_markup=back_to_menu(is_admin=True)
        )
        raise e


@router.callback_query(F.data.startswith("purchases_page_"), PurchasesStates.check_order)
async def get_next_page(callback: CallbackQuery, state: FSMContext, database: Database):
    page = int(callback.data.split("_")[-1])
    data = await state.get_data()

    start_date, end_date = data.get("start_date"), data.get("end_date")
    purchases = await database.purchases.get_by_date(start_date, end_date, page)
    pages = await database.purchases.get_pages_by_date(start_date, end_date)
    
    await callback.message.edit_text(
        text="Выберите заказ для просмотра подробной информации",
        reply_markup=purchases_pagination_keyboard(purchases, pages, page)
    )


@router.callback_query(F.data.startswith("purchase_"), PurchasesStates.check_order)
async def get_purchase(callback: CallbackQuery, state: FSMContext, database: Database):
    order_id = callback.data.split("_")[-1]
    print(order_id)
    purchase = await database.purchases.get_by_order_id(order_id)
    user: User = await database.users.get_item(purchase.tg_id)

    await state.update_data(order_id=order_id)
    await state.set_state(PurchasesStates.check_order)
    await callback.message.edit_text(
        text=format_purchase_data(purchase, json.loads(purchase.metadata_)),
        reply_markup=purchase_menu_keyboard(user.username)
    )


@router.callback_query(F.data == "search_by_order_id", PurchasesStates.choose_method)
async def search_by_order_id(callback: CallbackQuery, state: FSMContext):
    await state.set_state(PurchasesStates.input_order_id)
    await callback.message.edit_text(
        text="Введите номер заказа",
        reply_markup=back_to_menu(is_admin=True)
    )


@router.message(F.text, PurchasesStates.input_order_id)
async def input_order_id(message: Message, state: FSMContext, database: Database):
    order_id = message.text
    purchase = await database.purchases.get_by_order_id(order_id)

    if not purchase:
        await message.answer(
            text="Покупка не найдена",
            reply_markup=back_to_menu(is_admin=True)
        )
        return
    
    user = await database.users.get_item(purchase.tg_id)
    data = json.loads(purchase.metadata_)
    message_text = format_purchase_data(purchase, data)

    await state.update_data(order_id=order_id)
    await state.set_state(PurchasesStates.check_order)
    await message.answer(
        text=message_text,
        reply_markup=purchase_menu_keyboard(user.username)
    )


@router.callback_query(F.data == "change_status", PurchasesStates.check_order)
async def change_status(callback: CallbackQuery, state: FSMContext, database: Database):
    order_id = (await state.get_data()).get("order_id")
    purchase = await database.purchases.get_by_order_id(order_id)
    await state.set_state(PurchasesStates.set_status)
    await callback.message.edit_text(
        text="Выберите новый статус",
        reply_markup=change_status_keyboard(purchase.status)
    )


@router.callback_query(F.data.startswith("change_status_from_notification_"))
async def change_status_from_notificate(callback: CallbackQuery, state: FSMContext, database: Database):
    order_id = callback.data.split("_")[-1]
    purchase = await database.purchases.get_by_order_id(order_id)
    
    await state.update_data(order_id=order_id)
    await state.set_state(PurchasesStates.set_status)
    
    await callback.message.edit_text(
        text="Выберите новый статус",
        reply_markup=change_status_keyboard(purchase.status)
    )


@router.callback_query(PurchasesStates.set_status, F.data.startswith("set_"))
async def set_status(callback: CallbackQuery, state: FSMContext, database: Database):
    order_id = (await state.get_data()).get("order_id")
    status = callback.data.split("_")[-1]
    
    if status == "completed":
        purchase = await database.purchases.set_status(order_id, PurchaseStatuses.COMPLETED.value)
    elif status == "canceled":
        purchase = await database.purchases.set_status(order_id, PurchaseStatuses.CANCELED.value)
    else:
        purchase = await database.purchases.set_status(order_id, PurchaseStatuses.IN_PROGRESS.value)
    
    user = await database.users.get_item(purchase.tg_id)

    await state.set_state(PurchasesStates.check_order)
    await callback.message.edit_text(
        text=format_purchase_data(purchase, json.loads(purchase.metadata_)),
        reply_markup=purchase_menu_keyboard(user.username)
    )
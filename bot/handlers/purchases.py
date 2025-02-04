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
from keyboards.purchases import purchase_menu_keyboard, change_status_keyboard
from states.purchases import PurchasesStates
from database.db_main import Database


router = Router()


def format_purchase_data(purchase: Purchase, data: dict[str, str]) -> str:
        
    us_packs_info = [
        f"""
<b>Сумма</b>: {uc_pack['total_sum']} ₽
<b>Количество UC</b>: {uc_pack['uc_amount']} UC x {uc_pack['quantity']}
<b>Ошибки активации(Код → Ошибка)</b>:
{"\n".join([
    f"{err['uc_code']} → {err['message']}"
    for err in uc_pack['errors']
]) if uc_pack['errors'] else "Нет ошибок"}
""".strip()
        for uc_pack in data['uc_packs']
    ]
    
    message_text = f"""
<b>Заказ</b>: {purchase.payment_id}
<b>Дата покупки</b>: {(
        datetime
        .fromtimestamp(purchase.created_at / 1000)
        .strftime("%d.%m.%Y %H:%M:%S")
    )
}
<b>Игрок</b>: {purchase.player_id}
<b>Скидка</b>: {data['discount']} ₽
<b>Сумма UC</b>: {purchase.uc_sum} ₽
<b>Сумма заказа</b>: {purchase.price} ₽
<b>Метод оплаты</b>: {purchase.payment_method}
<b>Статус</b>: {purchase.status}

<b>Информация по UC-пакетам:</b>
{'\n\n'.join(us_packs_info)}
    """.strip()

    return message_text

@router.callback_query(F.data == "purchases")
async def purchases(callback: CallbackQuery, state: FSMContext, database: Database):
    await state.set_state(PurchasesStates.input_order_id)
    await callback.message.edit_text(
        text="Введите номер покупки",
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
    
    data = json.loads(purchase.metadata_)
    message_text = format_purchase_data(purchase, data)

    await state.update_data(order_id=order_id)
    await state.set_state(PurchasesStates.check_order)
    await message.answer(
        text=message_text,
        reply_markup=purchase_menu_keyboard(purchase.tg_id)
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


@router.callback_query(PurchasesStates.set_status, F.data.startswith("set_"))
async def set_status(callback: CallbackQuery, state: FSMContext, database: Database):
    order_id = (await state.get_data()).get("order_id")
    status = callback.data.split("_")[-1]
    
    if status == "completed":
        purchase = await database.purchases.set_status(order_id, PurchaseStatuses.COMPLETED.value)
    else:
        purchase = await database.purchases.set_status(order_id, PurchaseStatuses.IN_PROGRESS.value)

    await state.set_state(PurchasesStates.check_order)
    await callback.message.edit_text(
        text=format_purchase_data(purchase, json.loads(purchase.metadata_)),
        reply_markup=purchase_menu_keyboard(purchase.tg_id)
    )
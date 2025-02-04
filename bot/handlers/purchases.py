from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot.database.models.models import User
from bot.keyboards.commands import back_to_menu
from bot.keyboards.purchase import purchase_keyboard
from bot.states.purchases import PurchasesStates
from database.db_main import Database


router = Router()


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
    order = await database.purchases.get_by_order_id(order_id)
    if not order:
        await message.answer(
            text="Покупка не найдена",
            reply_markup=back_to_menu(is_admin=True)
        )
    else:
        await state.update_data(order_id=order_id)
        await state.set_state(PurchasesStates.check_order)
        await message.answer(
            text=order.metadata,
            reply_markup=purchase_keyboard(order.tg_id)
        )
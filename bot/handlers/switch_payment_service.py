from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_main import Database
from keyboards.commands import back_to_menu
from keyboards.switch_payment_service import switch_payment_service_keyboard
from states.menu import AdminMenuStates
from states.switch_payment_service import SwitchPaymentserviceStates


router = Router()


@router.callback_query(F.data == "switch_payment_service", AdminMenuStates.main)
async def choose_payment_service(callback: CallbackQuery, state: FSMContext, database: Database):
    settings = await database.settings.get_item()
    message_text = f"Выберите платежный сервис, текущий сервис: {settings.payment_service}"
    await state.set_state(SwitchPaymentserviceStates.choose_payment_service)
    await callback.message.edit_text(
        text=message_text,
        reply_markup=switch_payment_service_keyboard()
    )


@router.callback_query(SwitchPaymentserviceStates.choose_payment_service)
async def switch_payment_service(callback: CallbackQuery, state: FSMContext, database: Database):
    
    await database.settings.switch_payment_service(callback.data)
    await state.set_state(SwitchPaymentserviceStates.success)
    await callback.message.edit_text(
        text=f"Платежный сервис успешно изменен, текущий сервис: {callback.data}",
        reply_markup=back_to_menu(is_admin=True)
    )
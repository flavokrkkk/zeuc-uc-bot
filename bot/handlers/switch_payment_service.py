from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from bot.keyboards.switch_payment_service import switch_payment_service_keyboard


router = Router()


@router.callback_query(F.data == "switch_payment_service")
async def switch_payment_service(callback: CallbackQuery, state: FSMContext):
    message_text = "Выберите платежный сервис"
    await callback.message.edit_text(
        text=message_text,
        reply_markup=switch_payment_service_keyboard()
    )



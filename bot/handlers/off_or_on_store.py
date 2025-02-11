from aiogram import F, Router
from aiogram.types import CallbackQuery

from states.menu import AdminMenuStates
from database.db_main import Database
from keyboards.uc_stats import off_on_store_keyboard


router = Router()


@router.callback_query(F.data == "off_or_on_store", AdminMenuStates.main)
async def off_on_store(callback: CallbackQuery, database: Database):
    store_is_on = await database.settings.get_store_is_on()
    await callback.message.edit_text(
        text="Магазин сейчас включен" if store_is_on else "Магазин сейчас выключен",
        reply_markup=off_on_store_keyboard(store_is_on)
    )
    

@router.callback_query(F.data == "off_or_on_store_handle")
async def off_on_store_handle(callback: CallbackQuery, database: Database):
    store_is_on = await database.settings.update_store_is_on()
    await callback.message.edit_text(
        text="Магазин сейчас включен" if store_is_on else "Магазин сейчас выключен",
        reply_markup=off_on_store_keyboard(store_is_on)
    )
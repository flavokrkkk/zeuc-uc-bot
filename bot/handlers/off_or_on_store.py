from aiogram import Router
from aiogram.types import CallbackQuery


router = Router()


@router.callback_query(F.data == "off_or_on_store")
async def off_on_store(callback: CallbackQuery):
    pass
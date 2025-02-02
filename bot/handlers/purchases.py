from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from database.db_main import Database


router = Router()


@router.callback_query(F.data == "purchases")
async def get_payments(callback: CallbackQuery, state: FSMContext, database: Database):
    pass
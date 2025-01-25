from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from utils.filters import IsAdminFilter
from database.db_main import Database
from keyboards.commands import admin_menu_keyboard, main_menu_keyboard


router = Router()
    

@router.message(CommandStart())
async def start_bot(message: Message):
    message_text = """
    Это автоматический бот пополнения,
    который мгновенно доставит UC на ваш аккаунт 24/7
    """
    await message.answer(
        text=message_text,
        reply_markup=main_menu_keyboard(),
    )

    
@router.message(Command("admin"), IsAdminFilter())
async def admin_panel(message: Message, database: Database):
    message_text = "Вы находитесь в админ меню"
    await message.answer(
        text=message_text,
        reply_markup=admin_menu_keyboard()
    )
    

@router.message(Command("admin"), ~IsAdminFilter())
async def admin_panel_error(message: Message):
    message_text = "Вы не являетесь админом"
    await message.answer(message_text)
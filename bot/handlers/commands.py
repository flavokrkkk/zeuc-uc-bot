from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from keyboards.commands import main_menu_keyboard


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


@router.message(Command("/admin"))
async def admin_panel(message: Message):
    message_text = "Вы находитесь в админ меню"
    await message.answer(message_text)
    
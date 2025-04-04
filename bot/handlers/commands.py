from textwrap import dedent
from aiogram import F, Bot, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile, CallbackQuery, FSInputFile, InputFile, Message

from states.menu import AdminMenuStates
from utils.filters import IsAdminFilter
from database.db_main import Database
from keyboards.commands import admin_menu_keyboard, main_menu_keyboard


router = Router()
    

@router.message(CommandStart())
async def start_bot(message: Message, bot: Bot):
    message_text = dedent(
        """
        Это автоматический бот пополнения,
        который мгновенно доставит UC на ваш аккаунт 24/7
        """
    )
    with open("static/images/start_photo.jpg", "rb") as file:
        await message.answer_photo(
            photo=BufferedInputFile(file.read(), filename="start_photo.jpg"),
            caption=message_text,
            reply_markup=main_menu_keyboard(),
        )

    
@router.message(Command("admin"), IsAdminFilter())
async def admin_panel(message: Message, state: FSMContext):
    await state.set_state(AdminMenuStates.main)
    message_text = "Вы находитесь в админ меню"
    await message.answer(
        text=message_text,
        reply_markup=admin_menu_keyboard()
    )
    

@router.message(Command("admin"), ~IsAdminFilter())
async def admin_panel_error(message: Message):
    message_text = "Вы не являетесь админом"
    await message.answer(message_text)



@router.callback_query(F.data == "back_to_admin_menu")
async def back_to_admin_menu(callback: CallbackQuery, state: FSMContext):
    await state.set_state(AdminMenuStates.main)
    await callback.message.edit_text(
        text="Вы находитесь в админ меню",
        reply_markup=admin_menu_keyboard()
    )

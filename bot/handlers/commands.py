from aiogram import Router
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.utils.payload import decode_payload

from database.db_main import Database
from keyboards.commands import main_menu_keyboard


router = Router()


@router.message(CommandStart(deep_link=True))
async def start_with_deep_link(message: Message, command: CommandObject, database: Database):
    user = await database.users.get_item(item_id=message.from_user.id)
    *_, referer_id  = decode_payload(command.args).split('_')
    if not user and int(referer_id) != message.from_user.id:
        await database.users.add_item(
            tg_id=message.from_user.id, 
            username=message.from_user.username,
            referer_id=int(referer_id)
        )
    

@router.message(CommandStart())
async def start_bot(message: Message, database: Database):
    message_text = """
    Это автоматический бот пополнения,
    который мгновенно доставит UC на ваш аккаунт 24/7
    """
    user = await database.users.get_item(item_id=message.from_user.id)
    if not user:
        await database.users.add_item(
            tg_id=message.from_user.id, 
            username=message.from_user.username
        )
    await message.answer(
        text=message_text,
        reply_markup=main_menu_keyboard(),
    )


@router.message(Command("/admin"))
async def admin_panel(message: Message):
    message_text = "Вы находитесь в админ меню"
    await message.answer(message_text)
    
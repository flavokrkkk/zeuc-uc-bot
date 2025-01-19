from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.utils.deep_linking import create_start_link


router = Router()


@router.callback_query(F.data == "invite")
async def test(callback: CallbackQuery):
    link = await create_start_link(
        callback.bot,
        f'invite_to_zeus_{callback.from_user.id}',
        encode=True
    )
      
    await callback.message.answer(
        text=f'Ссылка для приглашения друга: {link}',
    )
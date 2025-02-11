from aiogram import F, Router
from aiogram.exceptions import TelegramBadRequest
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.menu import AdminMenuStates
from database.models.models import User
from keyboards.commands import back_to_menu
from states.black_list import BlackListStates
from database.db_main import Database
from keyboards.black_list import black_list_pagination


router = Router()


@router.callback_query(F.data == "black_list", AdminMenuStates.main)
async def get_black_list(callback: CallbackQuery, database: Database, state: FSMContext):
    users = await database.users.get_black_list()
    pages = await database.users.get_black_list_pages()
    await state.set_state(BlackListStates.check)
    await callback.message.edit_text(
        text="""
        Черный спиоск пользователей магазина, 
        чтобы удалить пользователя из списка нажмите 
        на него или нажмите на кнопку ниже и введите username
        """,
        reply_markup=black_list_pagination(users, pages, 1)
    )


@router.callback_query(F.data.startswith("black_list_page_"), BlackListStates.check)
async def get_black_list_next_page(callback: CallbackQuery, database: Database):
    try:
        page = int(callback.data.split("_")[-1])
        users = await database.users.get_black_list(page)
        pages = await database.users.get_black_list_pages()
        await callback.message.edit_text(
            text="""
            Черный спиоск пользователей магазина, 
            чтобы удалить пользователя из списка нажмите 
            на него или нажмите на кнопку ниже и введите username
            """,
            reply_markup=black_list_pagination(users, pages, page)
        )
    except TelegramBadRequest:
        await callback.answer()


@router.callback_query(F.data == "add_to_black_list", BlackListStates.check)
async def add_to_black_list(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BlackListStates.add_user_to_black_list)
    await callback.message.edit_text(
        text="Введите username пользователя, чтобы добавить его в черный список",
        reply_markup=back_to_menu(is_admin=True)
    )
    

@router.message(BlackListStates.add_user_to_black_list)
async def add_to_black_list_input(message: Message, database: Database):
    user = await database.users.get_by_username(message.text)
    if not user:
        await message.answer(
            text="Пользователь не найден",
            reply_markup=back_to_menu(is_admin=True)
        )
    else:
        username = await database.users.handle_black_list(user.tg_id, True)
        await message.answer(
            text=f"Пользователь {username} успешно добавлен в черный список",
            reply_markup=back_to_menu(is_admin=True)
        )


@router.callback_query(F.data == "remove_from_black_list", BlackListStates.check)
async def remove_from_black_list(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BlackListStates.remove_user_from_black_list)
    await callback.message.edit_text(
        text="Введите username пользователя, чтобы убрать его из черного списка"
    )


@router.message(BlackListStates.remove_user_from_black_list)
async def remove_from_black_list_input(message:  Message, state: FSMContext, database: Database):
    user = await database.users.get_by_username(message.text)
    if not user:
        await message.answer(
            text="Пользователь не найден",
            reply_markup=back_to_menu(is_admin=True)
        )
    else:
        username = await database.users.handle_black_list(user.tg_id, False)
        await message.answer(
            text=f"Пользователь {username} успешно удален из черного списка",
            reply_markup=back_to_menu(is_admin=True)
        )


@router.callback_query(F.data.startswith("black_list_user_"), BlackListStates.check)
async def remove_from_black_list_with_tg_id(callback: CallbackQuery, database: Database):
    user: User = await database.users.get_item(int(callback.data.split("_")[-1]))
    if not user:
        await callback.message.edit_text(
            text="Пользователь не найден",
            reply_markup=back_to_menu(is_admin=True)
        )
    else:
        username = await database.users.handle_black_list(user.tg_id, False)
        await callback.message.edit_text(
            text=f"Пользователь {username} успешно удален из черного списка",
            reply_markup=back_to_menu(is_admin=True)
        )
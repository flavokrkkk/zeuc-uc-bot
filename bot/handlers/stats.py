from datetime import datetime
from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from states.menu import AdminMenuStates
from states.stats import UCStatsState
from database.db_main import Database
from keyboards.commands import back_to_menu
from keyboards.uc_stats import get_stats_by_date_keyboard


router = Router()


@router.callback_query(F.data == "uc_stats", AdminMenuStates.main)
async def get_bot_stats(callback: CallbackQuery, state: FSMContext, database: Database):
    uc_stats = await database.purchases.get_stats()
    message_text = "\n".join(
        [
            f"{uc_amount} UC Packs: {sold_count}" 
            for uc_amount, sold_count in uc_stats.items()
        ]
    )
    await state.set_state(UCStatsState.check_default)
    await callback.message.edit_text(
        text=message_text if message_text else "Нет данных",
        reply_markup=get_stats_by_date_keyboard() if message_text else back_to_menu(is_admin=True)
    )


@router.callback_query(F.data == "get_by_date", UCStatsState.check_default)
async def get_by_date(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        text="Отправьте дату в формате ДД.ММ.ГГГГ - ДД.ММ.ГГГГ",
        reply_markup=back_to_menu(is_admin=True)
    )
    await state.set_state(UCStatsState.check_by_date)


@router.message(UCStatsState.check_by_date)
async def get_by_date(message: Message, state: FSMContext, database: Database):
    try:
        start_data, end_date = map(
            lambda x: int(
                datetime.strptime(x, "%d.%m.%Y").timestamp() * 1000
            ),
            message.text.split(" - ")
        )

        uc_stats = await database.purchases.get_stats(start_data, end_date)
        if not uc_stats:
            await message.answer(
                text="Нет данных за этот период",
                reply_markup=back_to_menu(is_admin=True)
            )
        else:
            message_text = "\n".join(
                [
                    f"{uc_amount} UC Packs: {sold_count}" 
                    for uc_amount, sold_count in uc_stats.items()
                ]
            )
            await message.answer(
                text=message_text,
                reply_markup=back_to_menu(is_admin=True)
            )
    except:
        await message.answer(
            text="Неверный формат даты",
            reply_markup=back_to_menu(is_admin=True)
        )

@router.callback_query(F.data == "bot_stats")
async def get_bot_stats(callback: CallbackQuery, state: FSMContext, database: Database):
    users_count = len(await database.users.get_all_items())
    users_who_buyed = await database.purchases.get_users_who_buyed()
    total_sum = await database.purchases.get_total_sum()

    message_text = (
        f"Пользователей: {users_count}\n"
        f"Пользователей, которые купили: {users_who_buyed}\n"
        f"Общая сумма продаж за все время: {total_sum}"
    )
    await callback.message.edit_text(
        text=message_text,
        reply_markup=back_to_menu(is_admin=True)
    )
    
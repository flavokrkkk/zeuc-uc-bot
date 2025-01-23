from aiogram.fsm.state import State, StatesGroup


class UCStatsState(StatesGroup):
    check_default = State()
    check_by_date = State()
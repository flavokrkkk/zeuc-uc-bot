from aiogram.fsm.state import State, StatesGroup


class BlackListStates(StatesGroup):
    check = State()
    add_user_to_black_list = State()
    remove_user_from_black_list = State()
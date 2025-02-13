from aiogram.fsm.state import State, StatesGroup


class UserRewardsStates(StatesGroup):
    input_username = State()
    input_date = State()
    check_by_username = State()
    choose_option = State()
    check_by_date = State()
    check_page = State()
    change_status = State()

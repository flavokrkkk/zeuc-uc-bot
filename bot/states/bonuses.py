from aiogram.fsm.state import State, StatesGroup


class AddBonusesStates(StatesGroup):
    input_username = State()
    input_amount = State()
    success = State()
from aiogram.fsm.state import State, StatesGroup


class PurchasesStates(StatesGroup):
    input_order_id = State()
    check_order = State()
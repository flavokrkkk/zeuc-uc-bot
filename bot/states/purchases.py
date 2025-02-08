from aiogram.fsm.state import State, StatesGroup


class PurchasesStates(StatesGroup):
    choose_method = State()
    input_date = State()
    input_order_id = State()
    check_order = State()
    set_status = State()
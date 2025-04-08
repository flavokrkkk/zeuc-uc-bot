from aiogram.fsm.state import State, StatesGroup


class SwitchPaymentserviceStates(StatesGroup):
    choose_payment_service = State()
    success = State()
from aiogram.fsm.state import State, StatesGroup


class UCCodesStates(StatesGroup):
    main = State()
    option = State()
    check_codes_by_value = State()
    delete_code = State()
    upload_codes = State()

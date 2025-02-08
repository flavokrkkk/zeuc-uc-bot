from aiogram.fsm.state import State, StatesGroup


class UCCodesStates(StatesGroup):
    main = State()
    option = State()
    check_codes_by_value = State()
    delete_code = State()
    upload_codes = State()
    success = State()
    change_price = State()
    

class AddNewPackStates(StatesGroup):
    add_uc_pack_amount = State()
    add_uc_pack_price = State()
    add_uc_pack_file = State()
    add_uc_pack_point = State()
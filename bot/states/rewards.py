from aiogram.fsm.state import State, StatesGroup


class RewardsStates(StatesGroup):
    choose = State()
    check_reward = State()
    change_uc_code = State()
    change_discount = State()
    choose_add_reward_type = State()


class AddUCPackReward(StatesGroup):
    choose_uc_pack = State()
    success = State()


class AddDiscountReward(StatesGroup):
    input_discount_value = State()
    input_min_payment_value = State()
    success = State()
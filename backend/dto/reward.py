from pydantic import BaseModel


class DiscountModel(BaseModel):
    discount_id: int
    value: int
    min_payment_value: int


class RewardModel(BaseModel):
    reward_id: int
    reward_type: str
    discount: DiscountModel | None = None
    uc_amount: int | None = None


class UpdateUserRewardsModel(BaseModel):
    reward_id: int
    player_id: int | None = None
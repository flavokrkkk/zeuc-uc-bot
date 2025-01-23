from pydantic import BaseModel

from backend.dto.uc_code_dto import UCCodeModel


class DiscountModel(BaseModel):
    discount_id: int
    value: int
    min_payment_value: int


class RewardModel(BaseModel):
    reward_id: int
    reward_type: str
    discount: DiscountModel | None = None
    uc_code: UCCodeModel | None = None


class UpdateUserRewardsModel(BaseModel):
    reward_id: int
    player_id: int
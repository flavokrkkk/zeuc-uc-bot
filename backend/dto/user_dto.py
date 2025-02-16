from datetime import datetime
from pydantic import BaseModel, field_validator

from backend.dto.reward import DiscountModel


class UserModel(BaseModel):
    username: str
    tg_id: int
    is_admin: bool
    bonuses: float
    referal_code: str
    balance: float
    referer_id: int | None = None
    

class UserDiscountModel(BaseModel):
    count: int
    discount: DiscountModel


class BonusesHistoryModel(BaseModel):
    amount: int
    status: str
    created_at: int | str

    @field_validator("created_at")
    def validate_created_at(cls, value: int):
        return datetime.fromtimestamp(value / 1000).strftime("%d.%m.%Y %H:%M:%S")


class UpdateUserBonusesModel(BaseModel):
    amount: int
    status: str


class UserForCircleBonusesModel(BaseModel):
    user: UserModel
    rewards_key: str
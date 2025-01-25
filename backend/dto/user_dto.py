from pydantic import BaseModel, field_validator

from backend.dto.reward import DiscountModel


class UserModel(BaseModel):
    username: str
    tg_id: int
    is_admin: bool
    bonuses: int
    referal_code: str
    balance: float
    referer_id: int | None = None
    

class UserDiscountModel(BaseModel):
    count: int
    discount: DiscountModel


class BonusesHistoryModel(BaseModel):
    amount: int
    created_at: int
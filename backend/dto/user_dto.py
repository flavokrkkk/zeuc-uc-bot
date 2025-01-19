from pydantic import BaseModel, field_validator

from backend.dto.reward import DiscountModel


class UserModel(BaseModel):
    username: str
    tg_id: int
    is_admin: bool
    bonuses: int


class UpdateUserModel(BaseModel):
    username: str
    

class UserDiscountModel(BaseModel):
    count: int
    discount: DiscountModel
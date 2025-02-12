from datetime import datetime
import json
from pydantic import BaseModel, field_validator


class BasePurchaseModel(BaseModel):
    tg_id: int
    player_id: int
    uc_sum: int
    price: int | float 
    payment_id: str | None = None
    payment_method: str | None = None
    is_paid: bool = False
    status: str
    created_at: int | str

    @field_validator("created_at")
    def validate_created_at(cls, value: int):
        return datetime.fromtimestamp(value / 1000).strftime("%d.%m.%Y %H:%M:%S")


class CreatePurchaseModel(BaseModel):
    tg_id: int
    player_id: int
    internal_order_id: str
    uc_sum: int
    price: int | float 
    payment_id: str | None = None
    payment_method: str | None = None
    is_paid: bool = False
    metadata_: dict | None = None


class PurchaseModel(BasePurchaseModel):
    internal_order_id: str
    metadata_: dict | str 

    @field_validator("metadata_")
    def validate_metadata(cls, value):
        if isinstance(value, str):
            return json.loads(value)
        return {}
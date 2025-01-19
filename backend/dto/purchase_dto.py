from pydantic import BaseModel


class CreatePurchaseModel(BaseModel):
    tg_id: int
    player_id: int
    uc_sum: int
    price: int | float 
    payment_id: str | None = None
    payment_method: str | None = None
    is_paid: bool = False
    metadata: dict | None = None


class PurchaseModel(BaseModel):
    tg_id: int
    player_id: int
    uc_sum: int
    price: int | float 
    payment_id: str | None = None
    payment_method: str | None = None
    is_paid: bool = False
    metadata: dict | None = None
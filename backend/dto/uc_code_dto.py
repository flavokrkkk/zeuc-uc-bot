from pydantic import BaseModel

from backend.dto.purchase_dto import PurchaseModel

    
class UCCodePrice(BaseModel):
    price: float
    point: int


class CreateUCCodeModel(BaseModel):
    code: str
    uc_amount: int
    price_per_uc: int


class UCCodeModel(BaseModel):
    ucinitial: int
    code: str
    price_per_uc: UCCodePrice
    total_sum: int = 0
    multiplication_uc: int = 0


class UCPackModel(BaseModel):
    uc_amount: int
    code: str
    price_per_uc: int
    total_sum: int
    count: int


class UCCodeGetBuyUrlModel(BaseModel):
    method_slug: str
    amount: int
    player_id: int
    uc_packs: list[UCPackModel]
    uc_sum: int
    discount: int = 0


class MetadataModel(BaseModel):
    tg_id: int
    player_id: int
    uc_packs: list[UCPackModel]
    notification_url: str
    internal_order_id: str
    discount: int = 0
    

class BuyUCCodeCallbackModel(BaseModel):
    order_id: str
    amount: float
    final_amount: float
    method: str
    metadata: MetadataModel


class UCActivationResult(BaseModel):
    success: int
    response: dict


class BuyUCCodeUrlModel(BaseModel):
    url: str
    order_id: str
    amount: float
    internal_id: str


class PaymentUCCodeDataModel(BaseModel):
    url: str
    order_id: str
    amount: float
    purchase: PurchaseModel
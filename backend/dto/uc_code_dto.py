from pydantic import BaseModel, Field

from backend.dto.purchase_dto import PurchaseModel

    
class UCCodePrice(BaseModel):
    price: float
    point: int


class CreateUCCodeModel(BaseModel):
    code: str
    uc_amount: int
    price_per_uc: int


class UCCodeModel(BaseModel):
    uc_amount: int
    price_per_uc: float
    quantity: int
    total_sum: int = 0
    multiplication_uc: int = 0
    point: int | None = None


class UCPackModel(BaseModel):
    uc_amount: int
    price_per_uc: int
    total_sum: int
    quantity: int
    activated_codes: int = 0
    errors: list[dict] = []
    error_activation_ids: list[str] = []


class UCCodeGetBuyUrlModel(BaseModel):
    method_slug: str
    amount: int
    player_id: int
    uc_packs: list[UCPackModel]
    uc_sum: int
    discount: int = 0


class BuyUCMetadataModel(BaseModel):
    tg_id: int
    player_id: int
    uc_packs: list[UCPackModel]
    notification_url: str
    internal_order_id: str
    discount: int = 0
    response: dict = {}


class BuyPointMetadataModel(BaseModel):
    tg_id: int
    point: int
    

class CodeepayBuyUCCodeCallbackModel(BaseModel):
    order_id: str
    amount: float
    final_amount: float
    method: str
    metadata: BuyUCMetadataModel


class BuyPointCallbackModel(BaseModel):
    metadata: BuyPointMetadataModel


class UCActivationError(BaseModel):
    status_code: int
    uc_code: str
    uc_amount: int
    price: int
    message: dict
    player_id: int


class UCActivateRequestModel(BaseModel):
    uc_code: str
    player_id: int
    uc_value: str


class BuyUCCodeUrlModel(BaseModel):
    url: str
    order_id: str
    amount: float = Field(exclude=True)
    internal_id: str = Field(exclude=True)


class PaymentUCCodeDataModel(BaseModel):
    url: str
    order_id: str
    amount: float
    purchase: PurchaseModel


class BuyPointModel(BaseModel):
    method_slug: str = "sbp"
    point: int
    amount: int
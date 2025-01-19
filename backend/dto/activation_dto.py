from pydantic import BaseModel
from backend.dto.purchase_dto import PurchaseModel


class CreateActivationModel(BaseModel):
    player_id: int
    uc_pack: str
    purchase_id: int | None = None



class ActivationModel(CreateActivationModel):
    purcase: PurchaseModel | None = None


class UCActivationResult(BaseModel):
    status: str
    message: str
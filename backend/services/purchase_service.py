import json
from backend.database.models.models import Purchase
from backend.dto.purchase_dto import CreatePurchaseModel, PurchaseModel
from backend.dto.uc_code_dto import BuyUCCodeUrlModel, BuyUCMetadataModel, PaymentUCCodeDataModel, UCCodeGetBuyUrlModel
from backend.dto.user_dto import UserModel
from backend.errors.purchase_errors import PurchaseNotFound
from backend.repositories.purchase_repository import PurchaseRepository
from backend.utils.config.enums import PurchaseStatuses


class PurchaseService:
    def __init__(self, repository: PurchaseRepository):
        self.repository = repository

    async def create_purchase(
        self, 
        form: UCCodeGetBuyUrlModel,
        current_user: UserModel,
        response: BuyUCCodeUrlModel
    ) -> None:
        new_purchase = CreatePurchaseModel(
            tg_id=current_user.tg_id,
            payment_id=response.order_id,
            internal_order_id=response.internal_id,
            uc_sum=form.uc_sum,
            price=form.amount - form.discount,
            payment_method=form.method_slug,
            player_id=form.player_id,
            metadata_={
                "tg_id": current_user.tg_id,
                "uc_packs": form.uc_packs,
                "discount": form.discount
            }
        )
        if new_purchase.metadata_:
            new_purchase.metadata_["uc_packs"] = [
                uc_pack.model_dump() 
                for uc_pack in new_purchase.metadata_["uc_packs"]
            ]
            new_purchase.metadata_ = json.dumps(new_purchase.metadata_)
        purchase = await self.repository.get_item(new_purchase.payment_id)
        if not purchase:
            purchase = await self.repository.add_item(**new_purchase.model_dump())

    async def get_by_tg_id(self, tg_id: int) -> list[PurchaseModel]:
        purchases = await self.repository.get_by_attributes((self.repository.model.tg_id, tg_id))
        return [
            PurchaseModel.model_validate(purchase, from_attributes=True) 
            for purchase in purchases
        ]

    async def mark_is_paid(
        self, 
        payment_id: str, 
        internal_order_id: str, 
        metadata: BuyUCMetadataModel
    ) -> PurchaseModel:
        purchase = await self.repository.get_by_attributes(
            (self.repository.model.payment_id, payment_id),
            (self.repository.model.internal_order_id, internal_order_id),
            one_or_none=True
        )
        if not purchase or purchase.is_paid:
            raise PurchaseNotFound
        
        return await self.repository.update_item(
            self.repository.model.payment_id, 
            payment_id, 
            is_paid=False,
            status=PurchaseStatuses.IN_PROGRESS.value,
            metadata_=json.dumps(metadata.model_dump(), ensure_ascii=False)
        )
    
    async def check_is_paid(self, order_id: str) -> bool | dict[str, str | int]:
        purchase: Purchase = await self.repository.get_by_attributes(
            (self.repository.model.payment_id, order_id),
            one_or_none=True
        )
        if not purchase or not purchase.is_paid:
            return False
        return json.loads(purchase.metadata_).get("response")
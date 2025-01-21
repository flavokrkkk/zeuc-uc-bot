import json
import random
import string
from backend.dto.purchase_dto import CreatePurchaseModel, PurchaseModel
from backend.dto.uc_code_dto import BuyUCCodeUrlModel, PaymentUCCodeDataModel
from backend.errors.purchase_errors import PurchaseNotFound
from backend.repositories.purchase_repository import PurchaseRepository
from backend.utils.config.enums import PurchaseStatuses


class PurchaseService:
    def __init__(self, repository: PurchaseRepository):
        self.repository = repository

    async def create_purchase(self, form: CreatePurchaseModel, codeepay_response: BuyUCCodeUrlModel) -> PurchaseModel:
        if form.metadata_:
            form.metadata_["uc_packs"] = [uc_pack.model_dump() for uc_pack in form.metadata_["uc_packs"]]
            form.metadata_ = json.dumps(form.metadata_)
        purchase = await self.repository.get_item(form.payment_id)
        if not purchase:
            purchase = await self.repository.add_item(**form.model_dump())
        purchase = PurchaseModel.model_validate(purchase, from_attributes=True)
        return PaymentUCCodeDataModel(
            url=codeepay_response.url,
            order_id=codeepay_response.order_id,
            amount=codeepay_response.amount,
            purchase=purchase
        )

    async def get_by_tg_id(self, tg_id: int) -> list[PurchaseModel]:
        purchases = await self.repository.get_by_attributes((self.repository.model.tg_id, tg_id))
        return [
            PurchaseModel.model_validate(purchase, from_attributes=True) 
            for purchase in purchases
        ]

    async def mark_is_paid(self, payment_id: str, internal_order_id: str) -> PurchaseModel:
        purchase = await self.repository.get_by_attributes(
            (self.repository.model.payment_id, payment_id),
            (self.repository.model.internal_order_id, internal_order_id),
            one_or_none=True
        )
        if not purchase or purchase.is_paid:
            raise PurchaseNotFound
        
        purchase = await self.repository.update_item(
            self.repository.model.payment_id, 
            payment_id, 
            is_paid=True,
            status=PurchaseStatuses.COMPLETED.value
        )
        return PurchaseModel.model_validate(purchase, from_attributes=True)
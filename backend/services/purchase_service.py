import json
import random
import string
from backend.dto.purchase_dto import CreatePurchaseModel, PurchaseModel
from backend.repositories.purchase_repository import PurchaseRepository


class PurchaseService:
    def __init__(self, repository: PurchaseRepository):
        self.repository = repository

    async def create_purchase(self, form: CreatePurchaseModel) -> PurchaseModel:
        if form.metadata:
            form.metadata = json.dumps(form.metadata).decode("utf-8")
        purchase = await self.repository.get_item(form.payment_id)
        if not purchase:
            purchase = await self.repository.add_item(**form.model_dump())
        return PurchaseModel.model_validate(purchase, from_attributes=True)

    async def get_by_tg_id(self, tg_id: int) -> list[PurchaseModel]:
        purchases = await self.repository.get_by_attributes((self.repository.model.tg_id, tg_id))
        return [
            PurchaseModel.model_validate(purchase, from_attributes=True) 
            for purchase in purchases
        ]

    async def mark_is_paid(self, payment_id: str) -> PurchaseModel:
        purchase = await self.repository.update_item(
            self.repository.model.payment_id, 
            payment_id, 
            is_paid=True
        )
        return PurchaseModel.model_validate(purchase, from_attributes=True)
import json
import random
import string
from backend.dto.purchase_dto import CreatePurchaseModel, PurchaseModel
from backend.repositories.purchase_repository import PurchaseRepository


class PurchaseService:
    def __init__(self, repository: PurchaseRepository):
        self.repository = repository

    def generate_payment_id() -> str:
        return "".join(random.choices(string.ascii_letters + string.digits, k=11))

    async def create_purchase(self, form: CreatePurchaseModel):
        if form.payment_id is None:
            form.payment_id = self.generate_payment_id()
        if form.metadata:
            form.metadata = json.dumps(form.metadata).decode("utf-8")
        purchase = await self.repository.get_item(form.payment_id)
        if not purchase:
            purchase = await self.repository.add_item(**form.model_dump())
        return PurchaseModel.model_validate(purchase, from_attributes=True)
    
    async def get_metadata(self, payment_id: str) -> dict:
        purchase = await self.repository.get_item(payment_id)
        if not purchase:
            return None
        if not purchase.metadata:
            return None
        return json.loads(purchase.metadata)
    
    async def set_metadata(self, payment_id: str, metadata: dict) -> None:
        purchase = await self.repository.get_item(payment_id)
        if not purchase:
            return None
        await self.repository.update_item(
            self.repository.model.payment_id, 
            payment_id, 
            metadata=json.dumps(metadata).decode()
        )

    async def get_all(self) -> list[PurchaseModel]:
        purchases = await self.repository.get_all_items()
        return [
            PurchaseModel.model_validate(purchase, from_attributes=True) 
            for purchase in purchases
        ]
    async def get_by_tg_id(self, tg_id: int) -> list[PurchaseModel]:
        purchases = await self.repository.get_by_attributes(
            (self.repository.model.tg_id, tg_id),
            one_or_none=True
        )
        return [
            PurchaseModel.model_validate(purchase, from_attributes=True) 
            for purchase in purchases
        ]
    
    async def delete_by_tg_id(self, tg_id: int) -> None:
        await self.repository.delete_by_attributes(
            (self.repository.model.tg_id, tg_id)
        )

    async def mark_is_paid(self, payment_id: str) -> None:
        await self.repository.update_item(
            self.repository.model.payment_id, 
            payment_id, 
            is_paid=True
        )
from backend.database.models.models import Purchase
from backend.dto.purchase_dto import CreatePurchaseModel, PurchaseModel
from backend.repositories.base import SqlAlchemyRepository


class PurchaseRepository(SqlAlchemyRepository):
    model = Purchase
    
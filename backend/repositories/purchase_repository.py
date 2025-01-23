from collections import defaultdict
from select import select

from sqlalchemy import func
from backend.database.models.models import Purchase
from backend.repositories.base import SqlAlchemyRepository


class PurchaseRepository(SqlAlchemyRepository):
    model = Purchase
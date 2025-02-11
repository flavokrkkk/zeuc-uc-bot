from database.models.models import Discount
from database.repositories.base import SqlAlchemyRepository


class DiscountRepository(SqlAlchemyRepository):
    model = Discount
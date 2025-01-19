from backend.database.models.models import UCCode
from backend.repositories.base import SqlAlchemyRepository


class UCCodeRepository(SqlAlchemyRepository):
    model = UCCode
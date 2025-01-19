from backend.database.models.models import Reward
from backend.repositories.base import SqlAlchemyRepository


class RewardRepository(SqlAlchemyRepository):
    model = Reward
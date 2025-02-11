from database.models.models import Reward
from database.repositories.base import SqlAlchemyRepository


class RewardRepository(SqlAlchemyRepository):
    model = Reward
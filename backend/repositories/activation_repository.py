from sqlalchemy import Result, select
from backend.database.models.models import Activation
from backend.repositories.base import SqlAlchemyRepository


class ActivationRepository(SqlAlchemyRepository):
    model = Activation

    async def get_between_by_value(self, value: int, start: int, end: int) -> list[Activation]:
        query = (
            select(self.model)
            .where(
                self.model.uc_pack == value, 
                self.model.created_at.between(start, end)
            )
        )
        activations: Result = await self.session.execute(query)
        return activations.scalars().all()
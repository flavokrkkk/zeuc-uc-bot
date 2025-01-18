from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from backend.database.models.base import Base
from backend.utils.config.config import db_config


class DatabaseConnection:
    def __init__(self):
        self._engine = create_async_engine(
            url=db_config.get_url()
        )

    async def get_session(self) -> AsyncSession:
        return AsyncSession(bind=self._engine)

    async def __call__(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        return self
    
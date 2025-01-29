from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from backend.database.connection.test_db import test_db
from backend.database.models.base import Base
from backend.utils.config.config import DB_CONFIG


class DatabaseConnection:
    def __init__(self):
        self._engine = create_async_engine(
            url=DB_CONFIG.get_url()
        )

    async def get_session(self) -> AsyncSession:
        return AsyncSession(bind=self._engine)

    async def __call__(self):
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            
        await test_db(await self.get_session())
        return self
    
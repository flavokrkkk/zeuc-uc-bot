from re import A
from sqlalchemy import ForeignKeyConstraint, Inspector, MetaData, Table, create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.schema import DropConstraint, DropTable
from backend.database.connection.test_db import test_admins, test_db
from backend.database.models.base import Base
from backend.utils.config.config import DB_CONFIG


class DatabaseConnection:
    def __init__(self):
        self._engine = create_async_engine(
            url=DB_CONFIG.get_url(is_async=True)
        )

    async def get_session(self) -> AsyncSession:
        return AsyncSession(bind=self._engine)
        
    async def __call__(self):
        async with self._engine.begin() as conn:
            if DB_CONFIG.DROP_DB:
                await conn.run_sync(Base.metadata.drop_all)
                await conn.run_sync(Base.metadata.create_all)
        return self
    
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


from utils.config.config import db_config


class DatabaseConnection:
    def __init__(self):
        self.engine = create_async_engine(
            url=db_config.get_url(),
            pool_size=100,
        )

    async def get_session(self) -> AsyncSession:
        return AsyncSession(self.engine)

from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.user import UserRepository


class Database:
    def __init__(self, session: AsyncSession) -> None:
        self.users: UserRepository = UserRepository(session=session)

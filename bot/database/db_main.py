from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.uc_code import UCCodeRepository
from database.repositories.user import UserRepository


class Database:
    def __init__(self, session: AsyncSession) -> None:
        self.users: UserRepository = UserRepository(session=session)
        self.uc_codes: UCCodeRepository = UCCodeRepository(session=session)

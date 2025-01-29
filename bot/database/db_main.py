from sqlalchemy.ext.asyncio import AsyncSession

from database.repositories.settigns import SettingsRepository
from database.repositories.purchase import PurchaseRepository
from database.repositories.uc_code import UCCodeRepository
from database.repositories.user import UserRepository


class Database:
    def __init__(self, session: AsyncSession) -> None:
        self.users = UserRepository(session=session)
        self.uc_codes= UCCodeRepository(session=session)
        self.purchases = PurchaseRepository(session=session)
        self.settings = SettingsRepository(session=session)

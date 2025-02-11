from sqlalchemy.ext.asyncio import AsyncSession

import database.repositories as repositories

class Database:
    def __init__(self, session: AsyncSession):
        self.users = repositories.UserRepository(session=session)
        self.uc_codes= repositories.UCCodeRepository(session=session)
        self.purchases = repositories.PurchaseRepository(session=session)
        self.settings = repositories.SettingsRepository(session=session)
        self.discounts = repositories.DiscountRepository(session=session)
        self.rewards = repositories.RewardRepository(session=session)
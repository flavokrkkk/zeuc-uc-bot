from environs import Env
from pydantic import BaseModel


class DatabaseConfig(BaseModel):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str
    DROP_DB: bool

    def get_url(self, is_async: bool = True) -> str:
        if is_async:
            return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


class JwtConfig(BaseModel):
    JWT_SECRET: str
    JWT_ALGORITHM: str
    JWT_ACCESS_TOKEN_TIME: int

env = Env()
env.read_env()


DB_CONFIG = DatabaseConfig(
    **{field: env.str(field.upper()) for field in DatabaseConfig.model_fields}
)
JWT_CONFIG = JwtConfig(
    **{field: env.str(field.upper()) for field in JwtConfig.model_fields}
)
BOT_TOKEN = env.str("BOT_TOKEN")
CODEEPAY_API_KEY = env.str("CODEEPAY_API_KEY")
UCODEIUM_API_KEY = env.str("UCODEIUM_API_KEY")
BONUS_CIRCLE_PRICE = 100
PAYMENT_NOTIFICATION_CHAT=-1002355857002
FREEKASSA_API_KEY = env.str("FREEKASSA_API_KEY")
FREEKASSA_API_SECRET_WORD = env.str("FREEKASSA_API_SECRET_WORD")
LAST_PURCHASE_ID = 0
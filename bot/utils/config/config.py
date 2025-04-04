from dataclasses import dataclass

from environs import Env
from pydantic import BaseModel


env = Env()
env.read_env()


class BotConfig(BaseModel):
    BOT_TOKEN: str


class DatabaseConfig(BaseModel):
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    DB_HOST: str
    DB_PORT: str

    def get_url(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


db_config = DatabaseConfig(
    **{field: env.str(field.upper()) for field in DatabaseConfig.model_fields}
)
bot_config = BotConfig(
    **{field: env.str(field.upper()) for field in BotConfig.model_fields}
)
WEB_APP_URL = env.str("WEBAPP_URL")
SUPPORT_URL = env.str("SUPPORT_URL")
REVIEWS_URL = env.str("REVIEWS_URL")
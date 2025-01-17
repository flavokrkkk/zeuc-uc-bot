from dataclasses import dataclass

from environs import Env


env = Env()
env.read_env()


@dataclass
class BotConfig:
    BOT_TOKEN: str


def load_bot_config() -> BotConfig:
    return BotConfig(BOT_TOKEN=env.str("BOT_TOKEN"))


def load_webapp_url() -> str:
    return env.str("WEBAPP_URL")
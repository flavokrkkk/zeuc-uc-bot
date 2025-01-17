from environs import Env
from pydantic import BaseModel


env = Env()
env.read_env()


class DatabaseConfig(BaseModel):
    db_name: str
    db_user: str
    db_pass: str
    db_host: str
    db_port: str


class JwtConfig(BaseModel):
    jwt_secret: str
    algorithm: str
    access_token_time: int


def load_database_config() -> DatabaseConfig:
    return DatabaseConfig(
        db_name=env.str("DB_NAME"),
        db_user=env.str("DB_USER"),
        db_pass=env.str("DB_PASS"),
        db_host=env.str("DB_HOST"),
        db_port=env.str("DB_PORT"),
    )


def load_jwt_config() -> JwtConfig:
    return JwtConfig(
        jwt_secret=env.str("JWT_SECRET"),
        algorithm=env.str("JWT_ALGORITHM"),
        access_token_time=int(env.str("JWT_ACCESS_TOKEN_TIME")),
    )
    
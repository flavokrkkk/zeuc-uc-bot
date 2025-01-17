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


class S3StorageConfig(BaseModel):
    bucket_name: str
    access_key_id: str
    secret_access_key: str
    region: str
    endpoint_url: str


def load_database_config() -> DatabaseConfig:
    return DatabaseConfig(
        db_name=env.str("DB_NAME"),
        db_user=env.str("DB_USER"),
        db_pass=env.str("DB_PASS"),
        db_host=env.str("DB_HOST"),
        db_port=env.str("DB_PORT"),
    )


def load_jwt_config() -> JwtConfig:
    env = Env()
    env.read_env()
    return JwtConfig(
        jwt_secret=env.str("JWT_SECRET"),
        algorithm=env.str("JWT_ALGORITHM"),
        access_token_time=int(env.str("JWT_ACCESS_TOKEN_TIME")),
    )


def load_s3_storage_config() -> S3StorageConfig:
    return S3StorageConfig(
        bucket_name=env.str("AWS_BUCKET_NAME"),
        access_key_id=env.str("AWS_ACCESS_KEY_ID"),
        secret_access_key=env.str("AWS_SECRET_ACCESS_KEY"),
        region=env.str("AWS_REGION"),
        endpoint_url=env.str("AWS_ENDPOINT_URL"),
    )


async def load_here_geocoding_api_key() -> str:
    return env.str("HERE_GEOCODING_API_KEY")

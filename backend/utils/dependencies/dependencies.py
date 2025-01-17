from functools import wraps
from time import perf_counter
from typing import Annotated, Any, AsyncGenerator, Awaitable, Callable, TypeVar, Union

from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.requests import HTTPConnection

import backend.services as services
import backend.repositories as repositories
from backend.dto.user_dto import BaseUserModel
from backend.services import AuthService
from backend.utils.clients.rabbit_client import RabbitClient
from backend.utils.clients.redis_client import RedisCache
from backend.utils.clients.s3_client import S3Client
from backend.utils.config.config import load_redis_config


bearer = HTTPBearer(auto_error=False)


R = TypeVar("R")


async def get_session(
    request: HTTPConnection,
) -> AsyncGenerator[AsyncSession, None]:
    session = await request.app.state.db_connection.get_session()
    try:
        yield session
    finally:
        await session.close()


async def get_auth_service(session=Depends(get_session)):
    return services.AuthService(repositories.UserRepository(session=session))


async def get_current_user_dependency(
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
    token: Annotated[HTTPBearer, Depends(bearer)],
) -> str:
    user = await auth_service.verify_token(token)
    user = await auth_service.check_user_exist(user)
    return user.id


async def get_user_service(session=Depends(get_session)):
    return services.UserService(repositories.UserRepository(session=session))
 
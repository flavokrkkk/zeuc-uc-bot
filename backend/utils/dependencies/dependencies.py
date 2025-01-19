from functools import wraps
from time import perf_counter
from typing import Annotated, AsyncGenerator

from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.requests import HTTPConnection

import backend.services as services
import backend.repositories as repositories
from backend.services import AuthService


bearer = HTTPBearer(auto_error=False)


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
) -> dict:
    user = await auth_service.verify_token(token)
    return user


async def get_user_service(session=Depends(get_session)):
    return services.UserService(repositories.UserRepository(session=session))
 

async def get_uc_code_service(session=Depends(get_session)):
    return services.UCCodeService(repositories.UCCodeRepository(session=session))


async def get_reward_service(session=Depends(get_session)):
    return services.RewardService(repositories.RewardRepository(session=session))


async def get_discount_service(session=Depends(get_session)):
    return services.DiscountService(repositories.DiscountRepository(session=session))


async def get_activation_service(session=Depends(get_session)):
    return services.ActivationService(repositories.ActivationRepository(session=session))
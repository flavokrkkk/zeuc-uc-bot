from typing import Annotated, AsyncGenerator

from aiogram import Bot
from asyncpg import TooManyConnectionsError
from fastapi import Depends, Request
from fastapi.security import HTTPBearer
from sqlalchemy.ext.asyncio.session import AsyncSession
from starlette.requests import HTTPConnection

from backend.database.connection.connection import DatabaseConnection
from backend.dto.user_dto import UserModel
from backend.errors.auth_errors import ManyRequestsError
import backend.services as services
import backend.repositories as repositories
from backend.utils.websocket.manager import WebsocketManager


bearer = HTTPBearer(auto_error=False)


async def get_bot(request: Request) -> Bot:
    return request.app.state.bot


async def get_session(
    request: HTTPConnection,
) -> AsyncGenerator[AsyncSession, None]:
    db_connection: DatabaseConnection = request.app.state.db_connection
    if await db_connection.get_opened_connections() >= 100:
        raise ManyRequestsError

    session = await db_connection.get_session()
    try:
        yield session
    except TooManyConnectionsError:
        raise ManyRequestsError
    finally:
        await session.close()


async def get_auth_service(session=Depends(get_session)) -> services.AuthService:
    return services.AuthService(repositories.UserRepository(session=session))


async def get_setting_service(session=Depends(get_session)) -> services.SettingService:
    return services.SettingService(repositories.SettingRepository(session=session))


async def get_current_user_dependency(
    auth_service: Annotated[services.AuthService, Depends(get_auth_service)],
    token: Annotated[HTTPBearer, Depends(bearer)],
) -> UserModel:
    return await auth_service.verify_token(token)


async def get_store_is_on(
    setting_service: Annotated[services.SettingService, Depends(get_setting_service)],
):
    return await setting_service.check_store_is_on()


async def get_user_service(session=Depends(get_session)) -> services.UserService:
    return services.UserService(repositories.UserRepository(session=session))
 

async def get_uc_code_service(session=Depends(get_session)) -> services.UCCodeService:
    return services.UCCodeService(repositories.UCCodeRepository(session=session))


async def get_reward_service(session=Depends(get_session)) -> services.RewardService:
    return services.RewardService(repositories.RewardRepository(session=session))


async def get_discount_service(session=Depends(get_session)) -> services.DiscountService:
    return services.DiscountService(repositories.DiscountRepository(session=session))


async def get_purchase_service(session=Depends(get_session)) -> services.PurchaseService:
    return services.PurchaseService(repositories.PurchaseRepository(session=session))


async def get_payment_service(session=Depends(get_session), bot=Depends(get_bot)) -> services.PaymentService:
    return services.PaymentService(
        bot=bot,
        repository=repositories.UCCodeRepository(session=session)
    )


async def get_websocket_manager() -> WebsocketManager:
    return WebsocketManager()
    
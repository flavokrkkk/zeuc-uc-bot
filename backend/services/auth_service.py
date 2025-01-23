from datetime import datetime, timedelta

from fastapi.security import HTTPBearer
from passlib.context import CryptContext

from jwt import decode, encode, InvalidTokenError
from backend.repositories.user_repository import UserRepository
from backend.dto.user_dto import UserModel
from backend.database.models.models import User
from backend.utils.config.config import jwt_config
from backend.errors.auth_errors import (
    InvalidToken,
    UserAlreadyNotRegister,
)

class AuthService:
    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def hash_password(self, password: str) -> str:
        return self.context.hash(password)

    async def authenticate_user(self, tg_id: int, username: str) -> User:
        user = await self.repository.get_by_attributes(
            (self.repository.model.tg_id, tg_id),
            (self.repository.model.username, username),
            one_or_none=True
        )
        if not user:
            raise UserAlreadyNotRegister
        return user

    async def create_access_token(self, username: str, tg_id: int) -> str:
        expire = datetime.now() + timedelta(
            minutes=jwt_config.JWT_ACCESS_TOKEN_TIME
        )
        data = {"sub": str(tg_id), "username": username, "exp": expire}
        token = encode(
            data, jwt_config.JWT_SECRET, algorithm=jwt_config.JWT_ALGORITHM
        )
        return token

    async def verify_token(self, token: HTTPBearer) -> dict[str, str]:
        try:
            payload = decode(
                token.credentials,
                jwt_config.JWT_SECRET,
                algorithms=[jwt_config.JWT_ALGORITHM],
            )
            tg_id = payload.get("sub")
            username = payload.get("username")

            if tg_id is None or username is None:
                raise InvalidToken
            
            user = await self.authenticate_user(tg_id=int(tg_id), username=username)
            return UserModel.model_validate(user, from_attributes=True)
        except (InvalidTokenError, AttributeError):
            raise InvalidToken

    async def check_user_exist(self, tg_id: int, username: str) -> User:
        user = await self.repository.get_by_attributes(
            (self.repository.model.tg_id, tg_id),
            (self.repository.model.username, username),
            one_or_none=True
        )
        if user is None: 
            raise InvalidToken
        return user

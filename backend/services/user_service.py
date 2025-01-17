from uuid import uuid4
from pydantic import UUID4

from backend.errors.user_errors import UserAlreadyHaveThisFriend, UserNotFound
from backend.database.models import User
from backend.dto.user_dto import BaseUserModel
from backend.repositories import UserRepository
from backend.services import BaseService


class UserService(BaseService):
    repository: UserRepository
    
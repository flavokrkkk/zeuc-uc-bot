from sqlalchemy import select, update

from backend.database.models import User
from backend.repositories.base import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User
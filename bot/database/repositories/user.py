from sqlalchemy import select, func
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.dialects.postgresql.operators import OVERLAP

from database.models.models import User
from database.repositories.base import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User

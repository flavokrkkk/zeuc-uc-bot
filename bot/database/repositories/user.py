from sqlalchemy import select, func, update
from sqlalchemy.dialects.postgresql import array
from sqlalchemy.dialects.postgresql.operators import OVERLAP

from database.models.models import User
from database.repositories.base import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository):
    model = User

    async def get_black_list_pages(self) -> int | None:
        pages_query = select(func.count()).select_from(self.model)
        pages = (await self.session.execute(pages_query)).scalar()
        return pages // 10 if pages // 10 else None

    async def get_black_list(self, page: int = 0) -> list[User]:
        users_query = (
            select(self.model)
            .where(self.model.in_black_list)
            .limit(10)
            .offset(page * 10)
        )
        users = (await self.session.execute(users_query)).scalars().all()
        return users
    
    async def get_by_username(self, username: str) -> User:
        query = select(self.model).where(self.model.username == username)
        return (await self.session.execute(query)).scalar_one_or_none()
    
    async def handle_black_list(self, tg_id: int, status: bool) -> str:
        query = (
            update(self.model)
            .where(self.model.tg_id == tg_id)
            .values(in_black_list=status)
            .returning(self.model.username)
        )
        username = (await self.session.execute(query)).scalar()
        await self.session.commit()
        return username
    
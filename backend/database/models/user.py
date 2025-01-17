from sqlalchemy.orm import Mapped, mapped_column
from backend.database.models.base import Base


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

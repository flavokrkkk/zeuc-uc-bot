from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column
from backend.database.models.base import Base


class UCCode(Base):
    __tablename__ = "uc_codes"

    code: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column(BigInteger)
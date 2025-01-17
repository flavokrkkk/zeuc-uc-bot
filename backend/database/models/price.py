from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from backend.database.models.base import Base


class Price(Base):
    __tablename__ = "prices"

    product: Mapped[str] = mapped_column(primary_key=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
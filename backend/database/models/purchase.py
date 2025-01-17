from sqlalchemy import BigInteger
from sqlalchemy.dialects.mysql import DECIMAL
from sqlalchemy.orm import Mapped, mapped_column
from backend.database.models.base import Base


class Purchase(Base):
    __tablename__ = "purchases"
    
    payment_id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    player_id: Mapped[int] = mapped_column(BigInteger)
    uc_sum: Mapped[int] = mapped_column(BigInteger)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    payment_method: Mapped[str] = mapped_column(nullable=True)
    is_paid: Mapped[bool] = mapped_column(default=False)
    metadata: Mapped[str] = mapped_column(nullable=True)

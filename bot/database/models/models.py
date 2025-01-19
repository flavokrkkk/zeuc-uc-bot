from sqlalchemy import DECIMAL, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.models.base import Base


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    referer_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    bonuses: Mapped[int] = mapped_column(BigInteger, default=0)


class Price(Base):
    __tablename__ = "prices"

    product: Mapped[str] = mapped_column(primary_key=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))


class Purchase(Base):
    __tablename__ = "purchases"
    
    payment_id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    player_id: Mapped[int] = mapped_column(BigInteger)
    uc_sum: Mapped[int] = mapped_column(BigInteger)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    payment_method: Mapped[str] = mapped_column(nullable=True)
    is_paid: Mapped[bool] = mapped_column(default=False)
    metadata_: Mapped[str] = mapped_column(nullable=True)

    activations: Mapped[list['Activation']] = relationship(
        back_populates='purchase', 
        cascade='all, delete-orphan'
    )


class UCCode(Base):
    __tablename__ = "uc_codes"

    code: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column(BigInteger)



class Activation(Base):
    __tablename__ = 'activations'

    activation_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    player_id: Mapped[int] = mapped_column(BigInteger, nullable=False)
    uc_pack: Mapped[str]
    purchase_id: Mapped[str] = mapped_column(
        ForeignKey('purchases.payment_id'), 
        nullable=False
    )

    purchase: Mapped['Purchase'] = relationship(back_populates='activations')
    
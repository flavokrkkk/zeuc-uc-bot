from uuid import uuid4
from sqlalchemy import DECIMAL, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database.models.base import Base
from backend.utils.config.enums import PurchaseStatuses


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    referer_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    bonuses: Mapped[int] = mapped_column(BigInteger, default=0)
    referal_code: Mapped[str] = mapped_column(default=str(uuid4()))

    discounts: Mapped[list['Discount']] = relationship(
        back_populates='users', 
        uselist=True, 
        secondary='user_discounts'
    )


class Price(Base):
    __tablename__ = "prices"

    price_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    point: Mapped[int]

    uc_codes: Mapped[list['UCCode']] = relationship(back_populates='price_per_uc')


class Purchase(Base):
    __tablename__ = "purchases"
    
    payment_id: Mapped[int] = mapped_column(primary_key=True)
    tg_id: Mapped[int] = mapped_column(BigInteger)
    player_id: Mapped[int] = mapped_column(BigInteger)
    uc_sum: Mapped[int] = mapped_column(BigInteger)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    payment_method: Mapped[str] = mapped_column(nullable=True)
    is_paid: Mapped[bool] = mapped_column(default=False)
    status: Mapped[bool] = mapped_column(default=PurchaseStatuses.IN_PROGRESS.value)
    metadata_: Mapped[str] = mapped_column(nullable=True)

    
class UCCode(Base):
    __tablename__ = "uc_codes"

    code: Mapped[str] = mapped_column(primary_key=True)
    ucinitial: Mapped[int]
    price_id: Mapped[str] = mapped_column(ForeignKey('prices.price_id'), nullable=True)
    
    price_per_uc: Mapped['Price'] = relationship(back_populates='uc_codes', lazy="selectin")
    rewards: Mapped[list['Reward']] = relationship(back_populates='uc_code', uselist=True)


class Discount(Base):
    __tablename__ = "discounts"

    discount_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    value: Mapped[int]
    min_payment_value: Mapped[int]

    rewards: Mapped[list['Reward']] = relationship(back_populates='discount', uselist=True)
    users: Mapped[list['User']] = relationship(
        back_populates='discounts', 
        uselist=True,
        secondary='user_discounts'
    )
    

class Reward(Base):
    __tablename__ = "scores"

    reward_id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    reward_type: Mapped[str]
    discount_id: Mapped[int] = mapped_column(ForeignKey('discounts.discount_id'), nullable=True)
    uc_pack_id: Mapped[str] = mapped_column(ForeignKey('uc_codes.code'), nullable=True)

    uc_code: Mapped['UCCode'] = relationship(back_populates='rewards', uselist=False, lazy="selectin")
    discount: Mapped['Discount'] = relationship(back_populates='rewards', uselist=False, lazy="selectin")


class UserDiscounts(Base):
    __tablename__ = "user_discounts"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'), primary_key=True)
    discount_id: Mapped[int] = mapped_column(ForeignKey('discounts.discount_id'), primary_key=True)
    count: Mapped[int] = mapped_column(default=0)
from sqlalchemy import DECIMAL, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database.models.base import Base


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    referer_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    bonuses: Mapped[int] = mapped_column(BigInteger, default=0)
    discounts: Mapped[list['Discount']] = relationship(
        back_populates='users', 
        uselist=True, 
        secondary='user_discounts'
    )


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
    ucinitial: Mapped[int]
    price_per_uc: Mapped[int]
    
    rewards: Mapped[list['Reward']] = relationship(back_populates='uc_code', uselist=True)


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
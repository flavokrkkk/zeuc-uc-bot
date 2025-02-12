from uuid import uuid4
from sqlalchemy import DECIMAL, BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database.models.base import Base
from backend.utils.config.enums import PurchaseStatuses


class Setting(Base):
    __tablename__ = "settings"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    store_is_on: Mapped[bool] = mapped_column(default=True)


class User(Base):
    __tablename__ = "users"

    tg_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    username: Mapped[str] = mapped_column(nullable=True)
    is_admin: Mapped[bool] = mapped_column(default=False)
    referer_id: Mapped[int] = mapped_column(BigInteger, nullable=True)
    bonuses: Mapped[float] = mapped_column(default=0.0)
    referal_code: Mapped[str] = mapped_column(default=lambda: str(uuid4()))
    balance: Mapped[float] = mapped_column(BigInteger, default=0)
    in_black_list: Mapped[bool] = mapped_column(default=False)
    
    discounts: Mapped[list['Discount']] = relationship(
        back_populates='users', 
        uselist=True, 
        secondary='user_discounts'
    )
    bonuses_history: Mapped[list['BonusesHistory']] = relationship(
        back_populates='user',
        uselist=True,
        lazy="selectin"
    )
    user_rewards: Mapped[list['UserRewards']] = relationship(
        back_populates='user',
        uselist=True,
        lazy="selectin"
    )


class BonusesHistory(Base):
    __tablename__ = "bonuses"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    tg_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))
    amount: Mapped[float]
    created_at: Mapped[int]
    status: Mapped[str]

    user: Mapped[User] = relationship(back_populates='bonuses_history')
    

class Price(Base):
    __tablename__ = "prices"

    price_id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    point: Mapped[int]

    uc_codes: Mapped[list['UCCode']] = relationship(back_populates='price_per_uc')


class Purchase(Base):
    __tablename__ = "purchases"
    
    payment_id: Mapped[str] = mapped_column(primary_key=True)
    internal_order_id: Mapped[str]
    tg_id: Mapped[int] = mapped_column(BigInteger)
    player_id: Mapped[int] = mapped_column(BigInteger)
    uc_sum: Mapped[int] = mapped_column(BigInteger)
    price: Mapped[float] = mapped_column(DECIMAL(10, 2))
    payment_method: Mapped[str] = mapped_column(nullable=True)
    is_paid: Mapped[bool] = mapped_column(default=False)
    status: Mapped[str] = mapped_column(default=PurchaseStatuses.IN_PROGRESS.value)
    metadata_: Mapped[str] = mapped_column(nullable=True)

    
class UCCode(Base):
    __tablename__ = "uc_codes"

    code: Mapped[str] = mapped_column(primary_key=True)
    uc_amount: Mapped[int]
    price_id: Mapped[str] = mapped_column(ForeignKey('prices.price_id'), nullable=True)
    
    price_per_uc: Mapped['Price'] = relationship(back_populates='uc_codes', lazy="selectin")


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
    uc_amount: Mapped[int] = mapped_column(nullable=True)
    
    discount: Mapped['Discount'] = relationship(back_populates='rewards', uselist=False, lazy="selectin")
    user_rewards: Mapped[list['UserRewards']] = relationship(back_populates='reward')


class UserDiscounts(Base):
    __tablename__ = "user_discounts"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'), primary_key=True)
    discount_id: Mapped[int] = mapped_column(ForeignKey('discounts.discount_id'), primary_key=True)
    count: Mapped[int] = mapped_column(default=0)


class UserRewards(Base):
    __tablename__ = "user_rewards"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.tg_id'))
    reward_id: Mapped[int] = mapped_column(ForeignKey('scores.reward_id'), nullable=True)
    secret_key: Mapped[str] 
    is_used: Mapped[bool] = mapped_column(default=False)

    user: Mapped['User'] = relationship(back_populates='user_rewards')
    reward: Mapped['Reward'] = relationship(back_populates='user_rewards')
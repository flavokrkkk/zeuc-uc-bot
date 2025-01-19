

from datetime import datetime
from sqlalchemy import BigInteger
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def get_current_timestamp():
    return int(datetime.now().timestamp() * 1000)


class Base(DeclarativeBase):
    created_at: Mapped[int] = mapped_column(BigInteger, default=get_current_timestamp())
    pass

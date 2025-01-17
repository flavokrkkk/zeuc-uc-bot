from sqlalchemy import Column, Integer, String, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from backend.database.models.base import Base


class Activation(Base):
    __tablename__ = 'activations'

    activation_id = Column(Integer, primary_key=True, autoincrement=True)
    tg_id = Column(Integer, nullable=False)
    player_id = Column(Integer, nullable=False)
    uc_pack = Column(Text, nullable=False)
    midas_login = Column(Text, nullable=True)
    midas_password = Column(Text, nullable=True)
    purchase_id = Column(String, ForeignKey('purchase.payment_id', ondelete='CASCADE'), nullable=False)

    purchase = relationship('Purchase', back_populates='activations')
    
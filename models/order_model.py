from ast import Str
from email.policy import default
from sqlalchemy import Column, Integer, String

from database import Base


class Order(Base):
    __tablename__ = 'orders'
    order_id = Column(Integer, primary_key=True)
    user_id = Column(Integer,  nullable=False)
    product_id = Column(Integer, nullable=False)
    count = Column(Integer, nullable=False, default=0)
    price = Column(Integer, nullable=False)
    status = Column(String(120), nullable=False)

    def __init__(self, user_id, product_id, count,  price, status):
        self.user_id = user_id
        self.product_id = product_id
        self.count = count
        self.price = price
        self.status = status

    def to_json(self):
        return {
            'id': self.order_id,
            'user_id': self.user_id,
            'product_id': self.product_id,
            'count': self.count,
            'price': self.price,
            'status':self.status
        }

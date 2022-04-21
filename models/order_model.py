from sqlalchemy import Column, Integer, String

from database import Base


class Order(Base):
    __tablename__ = 'Orders'
    order_id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    price = Column(Integer(), nullable=False)

    def __init__(self, name, price):
        self.name = name
        self.price = price

    def to_json(self):
        return {
            'id': self.order_id,
            'name': self.name,
            'price': self.price
        }

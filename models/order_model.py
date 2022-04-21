from sqlalchemy import Column, Integer, String

from database import Base


class Order(Base):
    __tablename__ = 'Orders'
    order_id = Column(Integer, primary_key=True)
    name = Column(String(120), nullable=False)
    user_id = Column(Integer, nullable=False)
    product_id = Column(Integer, nullable=False)
    price = Column(Integer(), nullable=False)

    def __init__(self, name, price, user_id, product_id):
        self.name = name
        self.user_id = user_id
        self.product_id = product_id
        self.price = price

    def to_json(self):
        return {
            'id': self.order_id,
            'name': self.name,
            'user_id': self.user_id,
            'product_id': self.order_id,
            'price': self.price
        }

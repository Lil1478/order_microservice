import re
from sqlalchemy.orm import validates
from fastapi import status, HTTPException

# from database import SessionLocal
from models.order_model import Order

# db = SessionLocal()


class OrderDAO:
    def __init__(self, ):
        self.collection_name = "Orders"

    def get_all(self):
        orders = db.query(Order).all()
        return orders

    def add_order(self, order: Order):
        order = Order(order.name, order.price)
        db.add(order)
        db.commit()
        return self.get_order(order.order_id)

    def get_order(self, order_id):
        order_db = db.query(Order).filter(Order.order_id == order_id).first()
        return order_db

    def delete_user(self, order_id):
        order_db = db.query(Order).filter(Order.order_id == order_id).first()
        if order_db is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource Not Found")
        db.delete(order_db)
        db.commit()
        return "SUCCESS"

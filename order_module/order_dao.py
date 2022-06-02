import re
from xxlimited import new
from sqlalchemy.orm import validates
from fastapi import status, HTTPException

from database import SessionLocal
from models.order_model import Order

db = SessionLocal()


class OrderDAO:
    def __init__(self, ):
        self.collection_name = "orders"

    def get_all(self):
        orders = db.query(Order).all()
        return orders

    def add_order(self, order: Order):
        db.add(order)
        db.commit()
        return self.get_order(order.order_id)

    def get_order(self, order_id):
        order_db = db.query(Order).filter(Order.order_id == order_id).first()
        return order_db

    def get_order_by_user_id(self, user_id):
        orders_db = db.query(Order).filter(Order.user_id == user_id).all()
        return orders_db

    def delete_order(self, order_id):
        order_db = db.query(Order).filter(Order.order_id == order_id).first()
        if order_db is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order Not Found")
        db.delete(order_db)
        db.commit()
        return "SUCCESS"

    def update_order(self, order_id, new_order:Order):
        db_order = db.query(Order).filter(Order.order_id == order_id).first()
        if db_order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order Not Found")
        db_order.user_id = new_order.user_id
        db_order.product_id = new_order.product_id
        db_order.count = new_order.count
        db_order.price = new_order.price
        return self.get_order(order_id)

    def update_order_status(self, order_id, new_status:str):
        db_order = db.query(Order).filter(Order.order_id == order_id).first()
        if db_order is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Order Not Found")
        db_order.status = new_status
        return self.get_order(order_id)

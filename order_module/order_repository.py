import requests

from models.order_model import Order


class OrderRepository:
    def __init__(self, account_dao):
        self.account_dao = account_dao
        print("OrderRepository")

    def add_order(self, order: Order):
        # return self.account_dao.add_order(order)
        return "order added"

    def get_orders(self):
        # return self.account_dao.get_all()
        return "order getted"

    def get_order_by_id(self, order_id):
        order = {"user_id": 1, "product_id": 1, "name": "order_1", "price": 1}

        user = requests.get('http://localhost:8000/users/%s' % order['user_id']).json()
        product = requests.get('http://localhost:4000/products/%s' % order['product_id']).json()

        print("user_id: " + str(user) + " producr_id" + str(product))

        return {"user_first_name": user['first_name'], "user_last_name": user['last_name'],
                "product_name": product['name'], "product_price": product['price']}
        # return self.account_dao.get_order(order_id)
        return "order getted by id"

    def delete_order(self, order_id):
        # return self.account_dao.delete_order(order_id)
        return "order deleted"

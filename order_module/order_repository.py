import configparser
import requests
from fastapi import APIRouter, status, HTTPException
from models.order_model import Order
from schemas.order_schemas import  StatusEnum

config = configparser.ConfigParser()
config.read('configuration.ini')
gateway_host = config['gateway']['products_host']


class OrderRepository:
    def __init__(self, order_dao):
        self.order_dao = order_dao
        print("OrderRepository")

    def add_order(self, user_id: int, order: Order):
        order = Order(user_id, order.product_id, order.count, order.price, "Nowe")

        new_order = self.order_dao.add_order(order)
        return new_order

    def get_orders(self):
        return self.order_dao.get_all()


    def get_order_by_user_id(self, checked_user):
        user_id = int(checked_user['user_id'])
        orders = self.order_dao.get_order_by_user_id(user_id)
        return orders

    def get_order_by_id(self, order_id):
        order = self.order_dao.get_order(order_id)
        order_json = order.to_json()

        product = requests.get(
            gateway_host + '/products/' + str(order_json['product_id'])).json()

        if product is None:
            return "NO_PRODUCT"
        return {
            'id': order.order_id,
            'user_id': order.user_id,
            'product': {
                'id': product['product_id'],
                "owner_id": product['owner_id'],
                'name': product['name'],
                'price': product['price'],
                'description': product['description']
            },
            'count': order.count,
            'price': order.price,

        }

    def update_order(self, order_id, new_order):
        return self.order_dao.update_order(order_id, new_order)

    def update_order_status(self, order_id, new_status):
        return self.order_dao.update_order_status(order_id, new_status)

    def delete_order(self, order_id):
        return self.order_dao.delete_order(order_id)


def check_user(request):
    gateway = config['gateway']['host']
    token = request.headers['Authorization']
    logged_user = requests.get(
        gateway + '/users/current', headers={'Authorization': token}).json()
    if 'detail' in logged_user:
        if logged_user['detail'] == 'Could not validate credentials':
            return "AUTH_ERROR"
    return logged_user

import configparser
import requests
from fastapi import APIRouter, status, HTTPException
from models.order_model import Order
from schemas.order_schemas import OrderDetailResponse, StatusEnum

config = configparser.ConfigParser()
config.read('configuration.ini')
gateway_host = config['gateway']['host']


class OrderRepository:
    def __init__(self, order_dao):
        self.order_dao = order_dao
        print("OrderRepository")

    def add_order(self, token, user_id: int, order: Order):
        product = requests.get(gateway_host + '/products/' + str(
            order.product_id), headers={'Authorization': token})
        product = product.json()
        if product is None:
            return "NO_PRODUCT"

        order = Order(user_id, order.product_id,
                      order.count, order.price, "Nowe")

        new_order = self.order_dao.add_order(order)
        return new_order

    def get_orders(self, token, detail):
        orders = self.order_dao.get_all()
        if detail:
            new_orders = []
            for order in orders:
                order_json = order.to_json()
                product = requests.get(gateway_host + '/products/' + str(
                    order_json['product_id']), headers={'Authorization': token})
                product = product.json()
                if product is None:
                    return "NO_PRODUCT"
                order_detail = OrderDetailResponse(
                    user_id=order.user_id, count=order.count, status=order.status, product=product, price=order.price, order_id=order.order_id)
                new_orders.append(order_detail)
            return new_orders
        return self.order_dao.get_all()

    def get_order_by_user_id(self, token, detail, checked_user):
        user_id = int(checked_user['user_id'])
        orders = self.order_dao.get_order_by_user_id(user_id)
        if detail:
            new_orders = []
            for order in orders:
                order_json = order.to_json()
                product = requests.get(gateway_host + '/products/' + str(
                    order_json['product_id']), headers={'Authorization': token})
                product = product.json()
                if product is None:
                    return "NO_PRODUCT"
                order_detail = OrderDetailResponse(
                    user_id=order.user_id, count=order.count, status=order.status, product=product, price=order.price, order_id=order.order_id)
                new_orders.append(order_detail)
            return new_orders
        return orders

    def get_order_by_id(self, token, detail, order_id):
        order = self.order_dao.get_order(order_id)
        order_json = order.to_json()

        if detail:
            product = requests.get(gateway_host + '/products/' + str(
                order_json['product_id']), headers={'Authorization': token})
            product = product.json()
            if product is None:
                return "NO_PRODUCT"

            order_detail = OrderDetailResponse(
                user_id=order.user_id, count=order.count, status=order.status, product=product, price=order.price, order_id=order.order_id)
            return order_detail
        return order_json

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

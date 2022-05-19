import requests

from models.order_model import Order


class OrderRepository:
    def __init__(self, order_dao):
        self.order_dao = order_dao
        print("OrderRepository")

    def add_order(self, user_id: int, order: Order):
        order = Order(user_id, order.product_id,
                      order.count, order.price)
        product = requests.get(
            'https://products-service-fihhyd5fhq-ew.a.run.app/products/' % order.product_id).json()

        new_order = self.order_dao.add_order(order)
        return {
            'id': new_order.order_id,
            'user_id': new_order.user_id,
            'product': {
                'id': product.product_id,
                "owner_id": product.owner_id,
                'name': product.name,
                'price': product.price,
                'description': product.description
            },
            'count': new_order.count,
            'price': new_order.price,

        }
        # return "order added"

    def get_orders(self):
        # return self.account_dao.get_all()
        return "order getted"

    def get_order_by_id(self, order_id):
        order = {"user_id": 1, "product_id": 1, "name": "order_1", "price": 1}

        # user = requests.get('http://localhost:8000/users/%s' %
        #                     order['user_id']).json()
        # product = requests.get(
        #     'http://localhost:4000/products/%s' % order['product_id']).json()

        # print("user_id: " + str(user) + " producr_id" + str(product))

        new_order = self.order_dao.get_order(order_id)
        order_json = new_order.to_json()
        print("$$$$$$$$$$$", order_json['product_id'])
        product = requests.get(
            'https://products-service-fihhyd5fhq-ew.a.run.app/products/' + str(order_json['product_id'])).json()
        return {
            'id': new_order.order_id,
            'user_id': new_order.user_id,
            'product': {
                'id': product['product_id'],
                "owner_id": product['owner_id'],
                'name': product['name'],
                'price': product['price'],
                'description': product['description']
            },
            'count': new_order.count,
            'price': new_order.price,

        }
        # return "order getted by id"

    def delete_order(self, order_id):
        # return self.order_dao.delete_order(order_id)
        return "order deleted"

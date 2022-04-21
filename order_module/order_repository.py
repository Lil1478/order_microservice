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
        # return self.account_dao.get_order(order_id)
        return "order getted by id"

    def delete_order(self, order_id):
        # return self.account_dao.delete_order(order_id)
        return "order deleted"

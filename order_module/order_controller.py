from fastapi import APIRouter
from starlette.requests import Request
import requests
import time

from order_module.order_dao import OrderDAO
from order_module.order_repository import OrderRepository
from schemas.order_schemas import Order
from helpers.rabbit import publish_message

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

# class OrderControllers:
#     def __init__(self, repository):
#         self.repository = repository
#         print('OrderControllers')

order_dao = OrderDAO()
order_repository = OrderRepository(order_dao)


@router.post("/")
async def add_order(request: Request, new_order: Order):
    data = await request.json()
    shipment_info = data["shipment_info"]
    user_id = 3
    r = requests.get(
        "https://is-gateway-v1-bi5g4x67.ew.gateway.dev/users/{}".format(user_id),
    )
    user_data = r.json()

    shipment_info["email"] = user_data["username"]
    # print(user_data)
    # user_id = requests.get('http://localhost:8000/users/%s' % body['user_id'])
    # product_id = requests.get(
    #     'https://is-gateway-v1-bi5g4x67.ew.gateway.dev/products/%s' % body['product_id'])
    # product = req.json()
    result = order_repository.add_order(user_id, new_order)
    publish_message(
        {
            "event": "created_order",
            "payload": {"order": result.to_json(), "shipment_info": shipment_info},
        }
    )
    return result


@router.get("/")
async def get_orders():
    return order_repository.get_orders()


@router.get("/{order_id}")
async def get_order(order_id: int):
    return order_repository.get_order_by_id(order_id)


@router.put("/{order_id}")
def update_order(order_id: int, new_order: Order):
    return {"order_name": new_order.name, "order_id": order_id}


@router.delete("/{order_id}")
async def delete_order(order_id: int):
    return order_repository.delete_order(order_id)

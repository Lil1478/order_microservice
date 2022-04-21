from fastapi import APIRouter
from starlette.requests import Request
import requests, time

from order_module.order_dao import OrderDAO
from order_module.order_repository import OrderRepository
from schemas.order_schemas import Order

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
    body = await request.json()

    # user_id = requests.get('http://localhost:8000/users/%s' % body['user_id'])
    # product_id = requests.get('http://localhost:4000/products/%s' % body['product_id'])
    # product = req.json()
    result = order_repository.add_order(new_order)
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

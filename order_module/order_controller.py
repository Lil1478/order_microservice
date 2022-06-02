import configparser
from fastapi import APIRouter, status, HTTPException
from starlette.requests import Request
import requests
import time

from order_module.order_dao import OrderDAO
from order_module.order_repository import OrderRepository, check_user
from schemas.order_schemas import Order

router = APIRouter(
    prefix="/orders",
    tags=["orders"],
    responses={404: {"description": "Not found"}},
)

order_dao = OrderDAO()
order_repository = OrderRepository(order_dao)

config = configparser.ConfigParser()
config.read('configuration.ini')
gateway_host = config['gateway']['host']

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


@router.post("/")
async def add_order(request: Request, new_order: Order):
    try:
        body = await request.json()
        checked_user = check_user(request)
        if checked_user == 'AUTH_ERROR':
            return credentials_exception
        user_id = int(checked_user['user_id'])
        result = order_repository.add_order(user_id, new_order)
        return result
    except:
        return "ERROR"


@router.get("/")
async def get_orders(request: Request):
    try:
        checked_user = check_user(request)
        if checked_user == 'AUTH_ERROR':
            return credentials_exception
        return order_repository.get_orders()
    except:
        return "ERROR"


@router.get("/{order_id}")
async def get_order(request: Request, order_id: int):
    try:
        checked_user = check_user(request)
        if checked_user == 'AUTH_ERROR':
            return credentials_exception
        return order_repository.get_order_by_id(order_id)
    except:
        return "ERROR"


@router.post("/user")
async def get_order_by_user_id(request: Request):
    checked_user = check_user(request)
    if checked_user == 'AUTH_ERROR':
        return credentials_exception
    return order_repository.get_order_by_user_id(checked_user)


@router.put("/{order_id}")
def update_order(request: Request, order_id: int, new_order: Order):

        checked_user = check_user(request)
        if checked_user == 'AUTH_ERROR':
            return credentials_exception
        return order_repository.update_order(order_id, new_order)



@router.put("/{order_id}/status")
async def update_order(request: Request, order_id: int):
        body = await request.json()
        checked_user = check_user(request)
        new_status = body['status']

        if checked_user == 'AUTH_ERROR':
            return credentials_exception
        return order_repository.update_order_status(order_id, new_status)


@router.delete("/{order_id}")
async def delete_order(request: Request, order_id: int):
    try:
        checked_user = check_user(request)
        if checked_user == 'AUTH_ERROR':
            return credentials_exception
        return order_repository.delete_order(order_id)
    except:
        return "ERROR"

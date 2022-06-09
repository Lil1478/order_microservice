import configparser
from fastapi import APIRouter, status, HTTPException
from starlette.requests import Request
import requests
import time

from order_module.order_dao import OrderDAO
from order_module.order_repository import OrderRepository, check_user
from schemas.order_schemas import Order
from helpers.rabbit import publish_message

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


@router.post("")
async def add_order(request: Request, new_order: Order):
    try:
        checked_user = check_user(request)
    except Exception as e:
        return HTTPException(
            status_code=500, detail="Error during processing")
    if checked_user == 'AUTH_ERROR':
        raise credentials_exception
    token = request.headers['Authorization']
    user_id = int(checked_user['user_id'])

    data = await request.json()
    shipment_info = data["shipment_info"]

    r = requests.get(
        "https://is-gateway-v1-bi5g4x67.ew.gateway.dev/users/{}".format(
            user_id), headers={'Authorization': token}
    )
    user_data = r.json()
    shipment_info["email"] = user_data["username"]

    result = order_repository.add_order(token, user_id, new_order)

    if result == "NO_PRODUCT":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product with such id is not exist")
    publish_message(
        {
            "event": "created_order",
            "payload": {"order": result.to_json(), "shipment_info": shipment_info},
        }
    )
    return result


@router.get("")
async def get_orders(request: Request, detail: bool = False):
    try:
        checked_user = check_user(request)
    except Exception as e:
        return HTTPException(
            status_code=500, detail="Error during processing")
    if checked_user == 'AUTH_ERROR':
        raise credentials_exception
    token = request.headers['Authorization']
    result = order_repository.get_orders(token, detail)
    if result == "NO_PRODUCT":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product with such id is not exist")
    return result


@router.get("/{order_id}")
async def get_order(request: Request, order_id: int,  detail: bool = False):
    try:
        checked_user = check_user(request)
    except Exception as e:
        return HTTPException(
            status_code=500, detail="Error during processing")
        if checked_user == 'AUTH_ERROR':
            raise credentials_exception
        token = request.headers['Authorization']
        result = order_repository.get_order_by_id(token, detail, order_id)
        if result == "NO_PRODUCT":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Product with such id is not exist")
        return result


@router.post("/user")
async def get_order_by_user_id(request: Request, detail: bool = False):
    try:
        checked_user = check_user(request)
    except Exception as e:
        return HTTPException(
            status_code=500, detail="Error during processing")
    if checked_user == 'AUTH_ERROR':
        raise credentials_exception
    token = request.headers['Authorization']
    result = order_repository.get_order_by_user_id(token, detail, checked_user)
    if result == "NO_PRODUCT":
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product with such id is not exist")
    return result


@router.put("/{order_id}")
def update_order(request: Request, order_id: int, new_order: Order):
    try:
        checked_user = check_user(request)
    except Exception as e:
        return HTTPException(
            status_code=500, detail="Error during processing")
    if checked_user == 'AUTH_ERROR':
        raise credentials_exception
    return order_repository.update_order(order_id, new_order)


@router.put("/{order_id}/status")
async def update_order_status(request: Request, order_id: int):
    try:
        body = await request.json()
        checked_user = check_user(request)
    except Exception as e:
        return HTTPException(
            status_code=500, detail="Error during processing")
    new_status = body['status']

    if checked_user == 'AUTH_ERROR':
        raise credentials_exception
    return order_repository.update_order_status(order_id, new_status)


@router.put("/{order_id}/shipment")
async def update_order_shipment(request: Request, order_id: int):
    try:
        body = await request.json()
        checked_user = check_user(request)
    except Exception as e:
        return HTTPException(
            status_code=500, detail="Error during processing")
    new_shipment_id = int(body['shipment_id'])

    if checked_user == 'AUTH_ERROR':
        raise credentials_exception
    return order_repository.update_order_shipment_id(order_id, new_shipment_id)


@router.delete("/{order_id}")
async def delete_order(request: Request, order_id: int):
    try:
        checked_user = check_user(request)
    except Exception as e:
        return HTTPException(
            status_code=500, detail="Error during processing")
    if checked_user == 'AUTH_ERROR':
        raise credentials_exception
    return order_repository.delete_order(order_id)

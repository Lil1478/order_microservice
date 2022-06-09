from enum import Enum
import string
from pydantic import BaseModel


class Order(BaseModel):
    product_id: int
    count: int
    price: float
    status: str


class OrderResponse(BaseModel):
    user_id: int
    count: int
    status: str
    product_id: int
    price: int
    order_id: int
    shipment_id: int


class Product(BaseModel):
    name: str
    description: str
    price: float
    product_id: int
    owner_id: int


class OrderDetailResponse(BaseModel):
    user_id: int
    count: int
    status: str
    product: Product
    price: int
    order_id: int


class StatusEnum(Enum):
    new = "Nowe"
    paid = "Opłacone"
    delivered = "Dostarczono"

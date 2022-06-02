from enum import Enum
import string
from pydantic import BaseModel


class Order(BaseModel):
    product_id: int
    count: int
    price: float


class StatusEnum(Enum):
    new = "Nowe"
    paid = "Opłacone"
    delivered = "Dostarczono"

from pydantic import BaseModel


class Order(BaseModel):
    name: str
    product_id: int
    count: int
    price: float

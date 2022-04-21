from pydantic import BaseModel


class Order(BaseModel):
    name: str
    user_id: int
    product_id: int
    price: float

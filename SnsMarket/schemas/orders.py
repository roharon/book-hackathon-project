from pydantic import BaseModel
from datetime import datetime


class Order(BaseModel):
    id: int
    user_id: int
    item_id: int
    quantity: int
    total_price: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class SingleOrder(BaseModel):
    data: Order


class OrderExists(BaseModel):
    data: bool

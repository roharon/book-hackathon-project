from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class Item(BaseModel):
    id: int
    market_id: int
    quantity: int
    price: int
    name: str
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class ItemBase(BaseModel):
    name: str
    price: int


class ItemCreate(ItemBase):
    market_id: int
    quantity: int


class ShowItem(BaseModel):
    data: Item


class ListItems(BaseModel):
    data: List[Optional[Item]]

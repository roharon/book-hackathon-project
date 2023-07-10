from typing import List
from pydantic import BaseModel
from schemas.menu import Menu


class CafeteriaBase(BaseModel):
    id: int
    name: str


class CafeteriaCreate(CafeteriaBase):
    pass


class CafeteriaUpdate(CafeteriaBase):
    pass


class CafeteriaWithMenus(BaseModel):
    id: int
    name: str
    menus: List[Menu]

    class Config:
        orm_mode = True

from pydantic import BaseModel


class MenuBase(BaseModel):
    description: str
    price: int


class MenuCreate(MenuBase):
    pass


class MenuUpdate(MenuBase):
    pass


class Menu(MenuBase):
    id: int

    class Config:
        orm_mode = True


class MenuInDBBase(MenuBase):
    id: int
    cafeteria_id: int
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

class MenuImageUpload(BaseModel):
    image_url: str

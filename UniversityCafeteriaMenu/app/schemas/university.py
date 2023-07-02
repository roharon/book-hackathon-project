from pydantic import BaseModel


class UniversityBase(BaseModel):
    name: str


class UniversityCreate(UniversityBase):
    pass


class UniversityUpdate(UniversityBase):
    pass


class UniversityInDBBase(UniversityBase):
    id: int
    name: str
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True

from pydantic import BaseModel


class Product(BaseModel):
    name: str
    description: str
    price: int

    class Config:
        orm_mode = True

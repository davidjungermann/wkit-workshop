from pydantic import BaseModel


class ProductRequest(BaseModel):
    name: str
    category: str
    price: int


class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: int

from datetime import datetime
from typing import Generator, List, Optional

from pydantic import BaseModel

from schemas.product import ProductResponse


class OrderRequest(BaseModel):
    products: List[int]
    quantities: List[int]


class OrderResponse(BaseModel):
    id: int
    timestamp: datetime
    total_price: int
    products: List[ProductResponse]

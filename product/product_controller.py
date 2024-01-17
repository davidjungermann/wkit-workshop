from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from db.session import get_db_session
from product.product_repository import ProductRepository
from product.product_service import ProductService
from schemas.product import ProductRequest, ProductResponse

router = APIRouter()


@router.post("/products", response_model=ProductResponse)
async def create_product(
    request: ProductRequest, db: Session = Depends(get_db_session)
) -> ProductResponse:
    product_service = ProductService(ProductRepository(db))
    return product_service.create_product(request)


@router.get("/products", response_model=List[ProductResponse])
async def get_products(db: Session = Depends(get_db_session)) -> List[ProductResponse]:
    product_service = ProductService(ProductRepository(db))
    return product_service.get_all_products()


@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int, db: Session = Depends(get_db_session)
) -> ProductResponse:
    product_service = ProductService(ProductRepository(db))
    product = product_service.get_product_by_id(product_id)
    return product

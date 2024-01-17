from typing import List

from fastapi import HTTPException

from product.product_repository import ProductRepository  # To be created
from schemas.product import ProductRequest, ProductResponse  # Your Pydantic models


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def create_product(self, request: ProductRequest) -> ProductResponse:
        product = self.repository.create_product(request.dict())
        if not product:
            raise HTTPException(404, "Product could not be created")
        return ProductResponse(
            id=product.id,
            name=product.name,
            category=product.category,
            price=product.price,
        )

    def get_all_products(self) -> List[ProductResponse]:
        products = self.repository.get_all_products()
        return [
            ProductResponse(id=p.id, name=p.name, category=p.category, price=p.price)
            for p in products
        ]

    def get_product_by_id(self, product_id: int) -> ProductResponse:
        product = self.repository.get_product_by_id(product_id)
        if not product:
            raise HTTPException(404, f"Product {product_id} not found")
        return ProductResponse(
            id=product.id,
            name=product.name,
            category=product.category,
            price=product.price,
        )

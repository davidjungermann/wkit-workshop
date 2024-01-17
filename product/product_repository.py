from typing import List, Optional

from sqlalchemy.orm import Session

from models.product import Product


class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_product(self, product_data: dict) -> Product:
        product = Product(**product_data)
        self.db.add(product)
        self.db.commit()
        self.db.refresh(product)
        return product

    def get_all_products(self) -> List[Product]:
        return self.db.query(Product).all()

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

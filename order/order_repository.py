from typing import List, Optional

from sqlalchemy.orm import Session
from sqlalchemy.sql.schema import Column

from models.order import Order, OrderDetail
from models.product import Product
from schemas.order import OrderRequest, OrderResponse, ProductResponse


class OrderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_order(self) -> Order:
        new_order = Order()
        self.db.add(new_order)
        self.db.commit()
        self.db.refresh(new_order)
        return new_order

    def add_order_detail(self, order_id: int, product_id: int, quantity: int):
        order_detail = OrderDetail(
            order_id=order_id, product_id=product_id, quantity=quantity
        )
        self.db.add(order_detail)
        self.db.commit()

    def update_order_total_price(self, order_id: int, total_price: int):
        order = self.db.query(Order).filter(Order.id == order_id).first()
        if order:
            order.total_price = total_price
            self.db.commit()

    def get_product_by_id(self, product_id: int) -> Optional[Product]:
        return self.db.query(Product).filter(Product.id == product_id).first()

    def get_all_orders(self) -> List[Order]:
        return self.db.query(Order).all()

    def get_order_by_id(self, order_id: int) -> Optional[Order]:
        return self.db.query(Order).filter(Order.id == order_id).first()

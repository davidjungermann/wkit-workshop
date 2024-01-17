from datetime import datetime
from typing import List

from sqlalchemy import Column, DateTime, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship

from db.database import Base
from models.product import Product

order_product_table = Table(
    "order_product",
    Base.metadata,
    Column("order_id", Integer, ForeignKey("orders.id"), primary_key=True),
    Column("product_id", Integer, ForeignKey("products.id"), primary_key=True),
)


class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    total_price = Column(Integer)
    products = relationship("Product", secondary=order_product_table)

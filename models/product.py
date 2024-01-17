from sqlalchemy import Column, Float, Integer, String

from . import Base


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    price = Column(Integer, nullable=False)

    # Add any additional fields or relationships here

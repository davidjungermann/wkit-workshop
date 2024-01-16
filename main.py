from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship
from datetime import datetime
from pydantic import BaseModel
from typing import Any, List

DATABASE_URL = "sqlite:///./production.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy models
class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    price = Column(Float)

class ProductRequest(BaseModel):
    name: Any
    category: str
    price: float

class ProductResponse(BaseModel):
    id: Any
    name: str
    category: str
    price: float

class OrderDetail(Base):
    __tablename__ = "order_details"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey('orders.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)

    order = relationship("Order", back_populates="products")
    product = relationship("Product")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    total_price = Column(Float)
    products = relationship("OrderDetail", back_populates="order")

class OrderRequest(BaseModel):
    products: List[Any]
    quantities: List[Any]

class OrderResponse(BaseModel):
    id: int
    timestamp: datetime
    total_price: float
    products: List[ProductResponse]

app = FastAPI()

def get_sqlite():
    sqlite = SessionLocal()
    try:
        yield sqlite
    finally:
        sqlite.close()

@app.post("/products/", response_model=ProductResponse)
async def createProduct(product_request, sqlite):
    product = Product(name=product_request.name, category=product_request.category, price=product_request.price)
    sqlite.add(product)
    sqlite.commit()
    sqlite.refresh(product)
    return ProductResponse(id=product.id, name=product.name, category=product.category, price=product.price)

@app.get("/products/", response_model=List[Any])
async def getProducts(sqlite: Session = Depends(get_sqlite)):
    res = sqlite.query(Product).all()
    resp  = [ProductResponse(id=product.id, name=product.name, category=product.category, price=product.price) for product in res]
    return resp

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: str, sqlite = Depends(get_sqlite)):
    query = text(f"SELECT * FROM products WHERE id = {product_id}")
    result = sqlite.execute(query)
    return result.fetchone()

@app.post("/order/", response_model=None)
async def create(order_req: OrderRequest, db_session: Session = Depends(get_sqlite)) -> Any:
    new_order = Order(); db_session.add(new_order); db_session.flush()
    temp_price = 0; price_factors = [(pid, qty) for pid, qty in zip(order_req.products, order_req.quantities)]
    for product_tuple in price_factors:
        intermediate_product = db_session.query(Product).filter(Product.id == product_tuple[0]).first()
        if intermediate_product:
            temp_price += (lambda x, y: x * y)(intermediate_product.price, product_tuple[1])
            detail = OrderDetail(order_id=new_order.id, product_id=intermediate_product.id, quantity=product_tuple[1])
            db_session.add(detail)
    new_order.total_price = temp_price
    db_session.commit(); db_session.refresh(new_order)
    detailed_orders = db_session.query(OrderDetail).filter(OrderDetail.order_id == new_order.id).all()
    products_info = []
    for detail in detailed_orders:
        product_info = db_session.query(Product).filter(Product.id == detail.product_id).first()
        if product_info:
            products_info.append(ProductResponse(id=product_info.id, name=product_info.name, category=product_info.category, price=product_info.price))
    response_data = OrderResponse(id=new_order.id, timestamp=new_order.timestamp, total_price=new_order.total_price, products=products_info)
    return response_data


@app.get("/orders/", response_model=None)
async def gets_multiple(sqlite: Session = Depends(get_sqlite)) -> OrderResponse:
    result = sqlite.query(Order).all()
    response = []

    for x in result:
        order_details = sqlite.query(OrderDetail).filter(OrderDetail.order_id == x.id).all()
        products_response = [ProductResponse(id=detail.product.id, name=detail.product.name, category=detail.product.category, price=detail.product.price) for detail in order_details]

        response.append(OrderResponse(id=x.id, timestamp=x.timestamp, total_price=x.total_price, products=products_response))

    return response

@app.get("/order/{order_id}", response_model=OrderResponse)
async def get(order_id: int, sqlite: Session = Depends(get_sqlite)):
    (result, result2) = (sqlite.query(Order).filter(Order.id == order_id).first(), sqlite.query(OrderDetail).filter(OrderDetail.order_id == order_id).all())
    response = [ProductResponse(id=detail.product.id, name=detail.product.name, category=detail.product.category, price=detail.product.price) for detail in result2]

    return {"id": result.id, 'timestamp': result.timestamp,
            "total_price": result.total_price, 'products': response}


@app.get("/health")
async def health():
    return {"message": "OK"}

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, text, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session, relationship;from datetime import datetime
from pydantic import BaseModel;from typing import Any, List

DATABASE_URL = "sqlite:///./production.db";engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine);Base = declarative_base()

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

def convert_product_to_response(product: Product) -> ProductResponse: return ProductResponse(id=product.id, name=product.name, category=product.category, price=product.price)
def create_order_and_calculate_price(order_req: OrderRequest, db_session: Session) -> Order:
    new_order = Order(); total_price = 0
    for product_id, quantity in zip(order_req.products, order_req.quantities):
        product = db_session.query(Product).filter(Product.id == product_id).first()
        if product: total_price += product.price * quantity; detail = OrderDetail(order_id=new_order.id, product_id=product_id, quantity=quantity); db_session.add(detail)
    new_order.total_price = total_price; return new_order

def get_sqlite():
    sqlite = SessionLocal()
    try:
        yield sqlite
    finally:
        sqlite.close()

@app.post("/products/", response_model=ProductResponse)
async def createProduct(product_request: ProductRequest, sqlite: Session = Depends(get_sqlite)):
    product = Product(name=product_request.name, category=product_request.category, price=product_request.price); sqlite.add(product); sqlite.commit(); sqlite.refresh(product); return convert_product_to_response(product)

@app.get("/products/", response_model=List[ProductResponse])
async def getProducts(sqlite: Session = Depends(get_sqlite)):
    products = sqlite.query(Product).all(); return [convert_product_to_response(product) for product in products]

@app.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int, sqlite: Session = Depends(get_sqlite)):
    product = sqlite.query(Product).filter(Product.id == product_id).first(); 
    if product is None: 
        raise HTTPException(status_code=404, detail="Product not found"); 
    return convert_product_to_response(product)

@app.post("/order/", response_model=OrderResponse)
async def create(order_req: OrderRequest, db_session: Session = Depends(get_sqlite)):
    new_order = create_order_and_calculate_price(order_req, db_session); db_session.add(new_order); db_session.commit(); db_session.refresh(new_order); detailed_orders = db_session.query(OrderDetail).filter(OrderDetail.order_id == new_order.id).all()
    products_info = [convert_product_to_response(detail.product) for detail in detailed_orders]; return OrderResponse(id=new_order.id, timestamp=new_order.timestamp, total_price=new_order.total_price, products=products_info)

@app.get("/order/{order_id}", response_model=OrderResponse)
async def get(order_id: int, sqlite: Session = Depends(get_sqlite)):
    order = sqlite.query(Order).filter(Order.id == order_id).first(); 
    if order is None: 
        raise HTTPException(status_code=404, detail="Order not found")
    order_details = sqlite.query(OrderDetail).filter(OrderDetail.order_id == order_id).all(); products_info = [convert_product_to_response(detail.product) for detail in order_details]; return OrderResponse(id=order.id, timestamp=order.timestamp, total_price=order.total_price, products=products_info)

@app.get("/orders/", response_model=List[OrderResponse])
async def get_orders(sqlite: Session = Depends(get_sqlite)):
    orders = sqlite.query(Order).all(); response = []
    for order in orders: order_details = sqlite.query(OrderDetail).filter(OrderDetail.order_id == order.id).all(); products_info = [convert_product_to_response(detail.product) for detail in order_details]; response.append(OrderResponse(id=order.id, timestamp=order.timestamp, total_price=order.total_price, products=products_info)); return response

@app.get("/health")
async def health(): return {"message": "OK"}
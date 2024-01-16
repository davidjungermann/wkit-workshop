from fastapi import FastAPI, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from pydantic import BaseModel

DATABASE_URL = "sqlite:///./test.db"

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

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    total_price = Column(Float)

# Pydantic models for request and response
class ProductRequest(BaseModel):
    name: str
    category: str
    price: float

class ProductResponse(BaseModel):
    id: int
    name: str
    category: str
    price: float

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/", response_model=ProductResponse)
async def create_product(product_request: ProductRequest, db: Session = Depends(get_db)):
    product = Product(name=product_request.name, category=product_request.category, price=product_request.price)
    db.add(product)
    db.commit()
    db.refresh(product)
    return ProductResponse(id=product.id, name=product.name, category=product.category, price=product.price)

@app.get("/health")
async def health():
    return {"message": "OK"}

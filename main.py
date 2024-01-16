from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Float, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import List

DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(DATABASE_URL)
Base = declarative_base()
metadata = MetaData()


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


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def read_root():
    return {"message": "Hello World"}


@app.post("/products/", response_model=Product)
async def create_product(product: Product, db: Session = Depends(get_db)):
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@app.get("/health")
async def health():
    return {"message": "OK"}

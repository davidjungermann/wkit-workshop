import random
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL
from db.database import Base
from models.order import Order, OrderDetail
from models.product import Product

# Create an engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Book categories (genres)
categories = [
    "Fiction",
    "Non-Fiction",
    "Science Fiction",
    "Fantasy",
    "Mystery",
    "Historical",
    "Biography",
    "Children's",
    "Self-Help",
    "Educational",
]

# List of 20 words to use in book titles
words = [
    "Secret",
    "Journey",
    "Mystery",
    "Lost",
    "Shadow",
    "Fire",
    "Dream",
    "Eternal",
    "Star",
    "Moon",
    "Heart",
    "Sky",
    "Ocean",
    "Whisper",
    "Legend",
    "Silent",
    "Wild",
    "Ancient",
    "Twilight",
    "Garden",
]


# Function to generate a creative book name
def generate_book_name():
    return " ".join(random.sample(words, 3))


# Function to create books
def create_books():
    db = SessionLocal()

    for _ in range(100):
        book_name = generate_book_name()
        category = random.choice(categories)
        price = round(random.uniform(5.99, 25.99), 2)

        book = Product(name=book_name, category=category, price=price)
        db.add(book)

    db.commit()
    db.close()


def create_orders():
    db = SessionLocal()

    products = db.query(Product).all()

    for _ in range(50):
        new_order = Order(timestamp=datetime.utcnow(), total_price=0)
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        total_price = 0
        for _ in range(random.randint(1, 5)):
            selected_product = random.choice(products)
            quantity = random.randint(1, 3)

            total_price += selected_product.price * quantity

            order_detail = OrderDetail(
                order_id=new_order.id, product_id=selected_product.id, quantity=quantity
            )
            db.add(order_detail)

        new_order.total_price = total_price
        db.commit()

    db.close()


def create_tables():
    Base.metadata.create_all(engine)


def main():
    create_tables()
    create_books()
    create_orders()


if __name__ == "__main__":
    main()

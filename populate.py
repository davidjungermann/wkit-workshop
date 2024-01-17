import random
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import DATABASE_URL
from db.database import Base
from models.order import Order
from models.product import Product

# Create an engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Book categories
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

# List of words for book titles
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


def generate_book_name():
    return " ".join(random.sample(words, 3))


def create_books():
    db = SessionLocal()
    for _ in range(100):
        book_name = generate_book_name()
        category = random.choice(categories)
        price = round(random.uniform(5.99, 25.99) * 100)  # Convert to cents
        book = Product(name=book_name, category=category, price=price)
        db.add(book)
    db.commit()
    db.close()


def create_orders():
    db = SessionLocal()
    products = db.query(Product).all()
    for _ in range(50):
        new_order = Order(timestamp=datetime.utcnow())
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        added_product_ids = set()  # Keep track of added products

        for _ in range(random.randint(1, 5)):
            selected_product = random.choice(products)

            if selected_product.id not in added_product_ids:
                new_order.products.append(selected_product)
                added_product_ids.add(selected_product.id)

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

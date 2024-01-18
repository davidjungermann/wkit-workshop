#
# Hej folk från WKIT! Ni behöver inte titta på denna fil.
# Den funkar tillräckligt bra! :)
#

import random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import Product, Base, DATABASE_URL, Order, OrderDetail

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

    # Create 100 book products
    for _ in range(100):
        book_name = generate_book_name()
        category = random.choice(categories)
        price = round(random.uniform(5.99, 25.99), 2)  # Prices between $5.99 and $25.99

        book = Product(name=book_name, category=category, price=price)
        db.add(book)

    # Commit the session to save changes
    db.commit()

    # Close the session
    db.close()


def create_orders():
    db = SessionLocal()

    # Retrieve all products for simplicity
    products = db.query(Product).all()
    num_products = len(products)

    # Create 50 orders
    for _ in range(50):
        new_order = Order(timestamp=datetime.utcnow())
        db.add(new_order)
        db.commit()
        db.refresh(new_order)

        # Randomly decide how many products this order will have
        num_order_products = random.randint(1, 5)  # Up to 5 products per order

        total_price = 0
        for _ in range(num_order_products):
            # Randomly select a product and quantity
            selected_product = random.choice(products)
            quantity = random.randint(1, 3)  # Up to 3 quantity per product

            # Calculate total price for this product
            total_price += selected_product.price * quantity

            # Create order detail
            order_detail = OrderDetail(
                order_id=new_order.id, product_id=selected_product.id, quantity=quantity
            )
            db.add(order_detail)

        # Update the total price of the order
        new_order.total_price = total_price
        db.commit()

    db.close()


# Function to create the tables
def create_tables():
    Base.metadata.create_all(engine)


# Main function
def main():
    create_tables()
    create_books()
    create_orders()


if __name__ == "__main__":
    main()

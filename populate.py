#
# Hej folk från WKIT! Ni behöver inte titta på denna fil.
# Den funkar som tänkt! :)
#

import random
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Reuse your existing model definitions and database URL
from main import Product, Base, DATABASE_URL  # Import from your FastAPI file

# Create an engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Book categories (genres)
categories = ["Fiction", "Non-Fiction", "Science Fiction", "Fantasy", "Mystery", "Historical", "Biography", "Children's", "Self-Help", "Educational"]

# List of 20 words to use in book titles
words = ["Secret", "Journey", "Mystery", "Lost", "Shadow", "Fire", "Dream", "Eternal", "Star", "Moon",
         "Heart", "Sky", "Ocean", "Whisper", "Legend", "Silent", "Wild", "Ancient", "Twilight", "Garden"]

# Function to generate a creative book name
def generate_book_name():
    return ' '.join(random.sample(words, 3))

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

# Function to create the tables
def create_tables():
    Base.metadata.create_all(engine)

# Main function
def main():
    create_tables()
    create_books()

if __name__ == "__main__":
    main()

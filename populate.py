# Hej WKIT! Denna filen behöver ni inte titta på. Den fungerar som den ska! :)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import random

# Reuse your existing model definitions and database URL
from main import Product, Order, Base, DATABASE_URL  # Import from your FastAPI file

# Create an engine and session
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# Function to create sample data
def create_sample_data():
    db = SessionLocal()

    # Create sample products
    products = [
        Product(name="Product 1", category="Category A", price=10.99),
        Product(name="Product 2", category="Category B", price=20.99),
        Product(name="Product 3", category="Category C", price=30.99)
    ]

    # Add products to the session
    db.add_all(products)

    # Create sample orders
    for _ in range(5):
        order = Order(timestamp=datetime.utcnow(), total_price=random.uniform(10.0, 100.0))
        db.add(order)

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
    create_sample_data()

if __name__ == "__main__":
    main()

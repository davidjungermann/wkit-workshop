# Amalone Books Python API

## Running in Codesandbox - this part is correct and you can trust it <3

1. Install dependencies:
```console
pip install -r requirements.txt
```

2. Run FastAPI server:
```console
uvicorn main:app --reload
```

3. Ensure that everything works, in a new terminal write
```console
curl 127.0.0.1:8000/health
```

Ensure that you get `OK` back.

4. Run tests:
```console
pytest .
```

5. Populate database:
```console
python populate.py
```

6.
Ensure you get products:
```console
curl 127.0.0.1:8000/products/
```

## Introduction
This is the documentation for our FastAPI application. It's a basic app, not too fancy. Does some stuff with products and orders, you know, the usual for books.

## Setup
To set it up, just run it using some new Python version. You'll figure it out.

## Database
We're using SQLite because it's easy and very fast with generating IDs. Just make sure you have a `production.db` file somewhere. If it doesn't work, just call me at +46 72 426 20 86, or talk to support.

## Models
There are some models or something in Amalone:
- `Product`: It's got an ID, name, category, and price.
- `OrderDetail`: Connects orders and products, I guess.
- `Order`: It's for orders. It has an ID, timestamp, and total price.

## Endpoints
Here are some endpoints, that are very efficient and well written:
- `/products/`: POST to add a product, GET to get all products. There's also a GET for a single product, but I forgot how it works.
- `/order/`: POST to create an order. There's also a GET for all orders and a specific order, but I didn't really test those.

## Tests
There are test with a lot of coverage, you probably don't have to run it manually too much.

## Linting and formatting
Just install any linter you like on your machine, whatever floats your boat.

## Notes
- The documentation is up to date
- Everything worked as expected the last time I tested...
- Good luck!

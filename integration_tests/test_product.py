from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# TODO: Let integration tests run towards dedicated database
def test_create_product():
    product_data = {
        "name": "Sample Product",
        "category": "Sample Category",
        "price": 100,
    }
    response = client.post("/products/", json=product_data)
    assert response.status_code == 200
    product_response = response.json()
    assert product_response["id"] is not None
    assert product_response["name"] == product_data["name"]
    assert product_response["category"] == product_data["category"]
    assert product_response["price"] == product_data["price"]


def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    products = response.json()
    assert isinstance(products, list)
    for product in products:
        assert "id" in product
        assert "name" in product
        assert "category" in product
        assert "price" in product


def test_get_product():
    product_id = 1  # Replace with a valid product ID
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 200
    product = response.json()
    assert "id" in product
    assert "name" in product
    assert "category" in product
    assert "price" in product


def test_get_product_not_found():
    product_id = 9999  # Assuming this product does not exist
    response = client.get(f"/products/{product_id}")
    assert response.status_code == 404


# More tests can be added as needed...

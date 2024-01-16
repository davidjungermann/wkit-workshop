from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    products = response.json()
    assert len(products) > 0

def test_get_product():
    response = client.get("/products/1")
    products = response.json()
    assert response

def test_create_order():
    response = client.post("order")
    assert response
    assert response.status_code

def test_get_orders():
    response = client.get("/orders/")
    assert response.status_code != 500
    products = response.json()
    assert len(products) > 0

def test_get_order():
    response = client.get("/products/1")
    products = response.json()
    assert response
    assert response.status_code == 200

def test_get_order_2():
    response = client.get("/order/2")
    products = response.json()
    assert response

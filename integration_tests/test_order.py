from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


# TODO: Let integration tests run towards dedicated database
def test_create_order():
    order_data = {
        "products": [1, 2],
        "quantities": [3, 4],
    }
    response = client.post("/orders/", json=order_data)
    assert response.status_code == 200
    order_response = response.json()
    assert order_response["id"] is not None
    assert isinstance(order_response["timestamp"], str)
    assert order_response["total_price"] is not None
    assert len(order_response["products"]) == len(order_data["products"])


def test_get_orders():
    response = client.get("/orders/")
    assert response.status_code == 200
    orders = response.json()
    assert isinstance(orders, list)
    for order in orders:
        assert "id" in order
        assert "timestamp" in order
        assert "total_price" in order
        assert "products" in order


def test_get_order():
    order_id = 1
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    order = response.json()
    assert "id" in order
    assert "timestamp" in order
    assert "total_price" in order
    assert "products" in order


def test_get_order_not_found():
    order_id = 9999
    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 404

import unittest
from unittest.mock import MagicMock

from fastapi import HTTPException

from order.order_repository import OrderRepository
from order.order_service import OrderService
from schemas.order import OrderRequest, OrderResponse, ProductResponse


class TestOrderService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MagicMock(spec=OrderRepository)
        self.order_service = OrderService(self.mock_repository)

    def test_create_order(self):
        # Mocking
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.timestamp = "2021-01-01T00:00:00"
        mock_order.total_price = 200
        self.mock_repository.create_order.return_value = mock_order

        mock_product = MagicMock()
        mock_product.id = 1
        mock_product.name = "Test Product"
        mock_product.category = "Test Category"
        mock_product.price = 100
        self.mock_repository.get_product_by_id.return_value = mock_product

        self.mock_repository.get_order_by_id.return_value = mock_order

        # Test
        order_request = OrderRequest(products=[1], quantities=[2])
        response = self.order_service.create_order(order_request)
        self.assertIsInstance(response, OrderResponse)
        self.assertEqual(response.id, 1)
        self.assertEqual(response.total_price, 200)

    def test_get_all_orders(self):
        # Mocking
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.timestamp = "2021-01-01T00:00:00"
        mock_order.total_price = 200
        self.mock_repository.get_all_orders.return_value = [mock_order]

        # Test
        orders = self.order_service.get_all_orders()
        self.assertIsInstance(orders, list)
        self.assertEqual(len(orders), 1)
        self.assertIsInstance(orders[0], OrderResponse)

    def test_get_order_by_id_found(self):
        # Mocking
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.timestamp = "2021-01-01T00:00:00"
        mock_order.total_price = 200
        self.mock_repository.get_order_by_id.return_value = mock_order

        # Test
        response = self.order_service.get_order_by_id(1)
        self.assertIsInstance(response, OrderResponse)
        self.assertEqual(response.id, 1)

    def test_get_order_by_id_not_found(self):
        # Mocking
        self.mock_repository.get_order_by_id.return_value = None

        # Test
        with self.assertRaises(HTTPException) as context:
            self.order_service.get_order_by_id(999)

        self.assertEqual(context.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()

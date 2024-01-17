import unittest
from unittest.mock import MagicMock

from fastapi import HTTPException

from product.product_repository import ProductRepository
from product.product_service import ProductService
from schemas.product import ProductRequest, ProductResponse


class TestProductService(unittest.TestCase):
    def setUp(self):
        self.mock_repository = MagicMock(spec=ProductRepository)
        self.product_service = ProductService(self.mock_repository)

    def test_create_product(self):
        # Mocking
        mock_product = MagicMock()
        mock_product.id = 1
        mock_product.name = "Test Product"
        mock_product.category = "Test Category"
        mock_product.price = 100
        self.mock_repository.create_product.return_value = mock_product

        # Test
        product_request = ProductRequest(
            name="Test Product", category="Test Category", price=100
        )
        response = self.product_service.create_product(product_request)
        self.assertIsInstance(response, ProductResponse)
        self.assertEqual(response.id, 1)
        self.assertEqual(response.name, "Test Product")
        self.assertEqual(response.category, "Test Category")
        self.assertEqual(response.price, 100)

    def test_get_all_products(self):
        # Mocking
        mock_product = MagicMock()
        mock_product.id = 1
        mock_product.name = "Test Product"
        mock_product.category = "Test Category"
        mock_product.price = 100
        self.mock_repository.get_all_products.return_value = [mock_product]

        # Test
        products = self.product_service.get_all_products()
        self.assertIsInstance(products, list)
        self.assertEqual(len(products), 1)
        self.assertIsInstance(products[0], ProductResponse)

    def test_get_product_by_id_found(self):
        # Mocking
        mock_product = MagicMock()
        mock_product.id = 1
        mock_product.name = "Test Product"
        mock_product.category = "Test Category"
        mock_product.price = 100
        self.mock_repository.get_product_by_id.return_value = mock_product

        # Test
        response = self.product_service.get_product_by_id(1)
        self.assertIsInstance(response, ProductResponse)
        self.assertEqual(response.id, 1)

    def test_get_product_by_id_not_found(self):
        # Mocking
        self.mock_repository.get_product_by_id.return_value = None

        # Test
        with self.assertRaises(HTTPException) as context:
            self.product_service.get_product_by_id(999)

        self.assertEqual(context.exception.status_code, 404)


if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import MagicMock, patch
from main import create_order_and_calculate_price, OrderRequest, Order


class TestCreateOrderAndCalculatePrice(unittest.TestCase):
    @patch("main.Session")
    def test_order_creation_and_price_calculation(self, mock_session):
        # Arrange
        mock_db = mock_session.return_value
        mock_query = mock_db.query.return_value
        mock_filter = mock_query.filter.return_value
        mock_first = mock_filter.first.side_effect = [
            MagicMock(price=100.0),
            MagicMock(price=200.0),
        ]

        order_request = OrderRequest(products=[1, 2], quantities=[2, 3])

        # Act
        new_order = create_order_and_calculate_price(order_request, mock_db)

        # Assert
        self.assertIsInstance(new_order, Order)
        expected_total_price = (2 * 100.0) + (
            3 * 200.0
        )  # 2x Product 1 and 3x Product 2
        self.assertEqual(new_order.total_price, expected_total_price)

        # Verify that add method was called the expected number of times
        self.assertEqual(
            mock_db.add.call_count, 2
        )  # 2 OrderDetail objects + 1 Order object


if __name__ == "__main__":
    unittest.main()

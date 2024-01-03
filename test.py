import unittest
from sum import sum


class TestSum(unittest.TestCase):

    def test_sum(self):
        num1 = 3
        num2 = 3
        self.assertEqual(sum(num1, num2), 6)


if __name__ == '__main__':
    unittest.main()

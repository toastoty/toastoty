
import unittest
from main import main_test


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(main_test(),0.99)   #首先假设预测的是前面第一组运行的测试数据


if __name__ == '__main__':
    unittest.main()


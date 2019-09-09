import sys
sys.path.append(r'C:\Users\Aaron\PycharmProjects\BoardGame')
from display.text_api import _transpose
import unittest


class TestTextApi(unittest.TestCase):

    def test_transpose(self):
        pre = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
        expected = [[1, 4, 7, 10], [2, 5, 8, 11], [3, 6, 9, 12]]
        self.assertEqual(expected, _transpose(pre))


if __name__ == '__main__':
    unittest.main()

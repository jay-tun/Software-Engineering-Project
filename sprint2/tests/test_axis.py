import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('../src/wdc')
from wdc import Axis

class TestAxis(unittest.TestCase):
    def test_single_point_axis(self):
        # Test initialization with a single point axis
        axis = Axis("time", 2024)
        self.assertEqual(str(axis), "time(2024)")

    def test_range_axis(self):
        # Test initialization with a range axis
        axis = Axis("latitude", 40, 50)
        self.assertEqual(str(axis), "latitude(40:50)")

    def test_upper_bound_none(self):
        # Test initialization with upper_bound as None
        axis = Axis("depth", 0)
        self.assertEqual(str(axis), "depth(0)")

if __name__ == '__main__':
    unittest.main()

import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('../src/wdc')
from wdc import RGBColor

class TestRGBColor(unittest.TestCase):
    def test_initialization(self):
        # Test initialization of RGBColor instance
        color = RGBColor(100, 150, 200)
        self.assertEqual(color.red, 100)
        self.assertEqual(color.green, 150)
        self.assertEqual(color.blue, 200)

    def test_string_representation(self):
        # Test string representation of RGBColor instance
        color = RGBColor(100, 150, 200)
        self.assertEqual(str(color), "{red: 100; green: 150; blue: 200}")

if __name__ == '__main__':
    unittest.main()
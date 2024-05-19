import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('../src/wdc')
from wdc import Coverage, Axis, BinaryOperation

class TestCoverage(unittest.TestCase):
    def setUp(self):
        # Reset coverage counter for each test
        Coverage.coverage_counter = 1
        
        # Initialize some Coverage instances for testing
        self.coverage1 = Coverage("Temperature")
        self.coverage2 = Coverage("Rainfall")

    def test_unique_variable_assignment(self):
        # Test that the unique variable is correctly assigned
        self.assertEqual(self.coverage1.variable, 'c1')
        self.assertEqual(self.coverage2.variable, 'c2')

    def test_subset_setting(self):
        # Test setting and getting subset parameters
        axis1 = Axis("Lat", 53.08)
        axis2 = Axis("Long", 8.80)
        self.coverage1.set_subset(axis1, axis2)
        self.assertEqual(self.coverage1.subset, '[Lat(53.08), Long(8.8)]')

    def test_arithmetic_operations(self):
        # Test arithmetic operations between Coverage instances
        result = self.coverage1 + self.coverage2
        self.assertIsInstance(result, BinaryOperation)
        self.assertEqual(str(result), '($c1 + $c2)')

    def test_comparison_operations(self):
        # Test comparison operations between Coverage instances
        result = self.coverage1 == self.coverage2
        self.assertIsInstance(result, BinaryOperation)
        self.assertEqual(str(result), '($c1 = $c2)')

    def test_mixed_operations(self):
        # Test mixed arithmetic and comparison operations
        result = self.coverage1 + self.coverage2 * 2
        self.assertIsInstance(result, BinaryOperation)
        self.assertEqual(str(result), '($c1 + ($c2 * 2))')

if __name__ == '__main__':
    unittest.main()


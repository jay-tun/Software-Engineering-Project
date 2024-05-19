import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('../src/wdc')
from wdc import BinaryOperation, Coverage

class TestBinaryOperation(unittest.TestCase):
    def setUp(self):
        # Reset coverage counter for each test
        Coverage.coverage_counter = 1
        
        # Initialize some Coverage instances for testing
        self.coverage1 = Coverage("Temperature")
        self.coverage2 = Coverage("Rainfall")

    def test_str_representation(self):
        # Test string representation of a binary operation
        operation = BinaryOperation(self.coverage1, '+', self.coverage2)
        self.assertEqual(str(operation), '($c1 + $c2)')

    def test_arithmetic_operations(self):
        # Test arithmetic operations between two coverages
        operation = self.coverage1 + self.coverage2
        self.assertIsInstance(operation, BinaryOperation)
        self.assertEqual(str(operation), '($c1 + $c2)')

    def test_equal_operation(self):
        # Test equal operation to see if == is replaced with an =
        operation = self.coverage1 == self.coverage2
        self.assertIsInstance(operation, BinaryOperation)
        self.assertEqual(str(operation), '($c1 = $c2)')
        
    def test_comparison_operatios(self):
        # Test comparison operators like >
        operation = self.coverage1 > self.coverage2
        self.assertIsInstance(operation, BinaryOperation)
        self.assertEqual(str(operation), '($c1 > $c2)')

if __name__ == '__main__':
    unittest.main()

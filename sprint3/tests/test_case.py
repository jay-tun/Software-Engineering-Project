import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('../src/wdc')
from wdc import Case, RGBColor, Coverage, BinaryOperation, Axis

class TestCase(unittest.TestCase):
    def setUp(self):
        # Reset coverage counter for each test
        Coverage.coverage_counter = 1
        
        # Initialize an RGBColor instance for testing
        self.color = RGBColor(100, 150, 200)

    def test_initialization(self):
        # Test initialization of Case instance with a string expression
        case = Case("temperature > 30", self.color)
        self.assertEqual(case.expression, "temperature > 30")
        self.assertEqual(case.RGBColor, self.color)

        # Test initialization of Case instance with a BinaryOperation expression
        binary_operation = BinaryOperation("temperature", ">", 30)
        case = Case(binary_operation, self.color)
        self.assertEqual(case.expression, binary_operation)
        self.assertEqual(case.RGBColor, self.color)

    def test_string_representation(self):
        # Test string representation of Case instance
        case = Case("temperature > 30", self.color)
        expected_str = "case temperature > 30\n\t\treturn {red: 100; green: 150; blue: 200}"
        self.assertEqual(str(case), expected_str)
        
    def test_with_coverage(self):
        # Test the case when using a Coverage instance
        coverage1 = Coverage("Temperature")
        case = Case(coverage1 > 50, self.color)
        expected_str = "case ($c1 > 50)\n\t\treturn {red: 100; green: 150; blue: 200}"
        self.assertEqual(str(case), expected_str)
        
    def test_with_coverage_subset(self):
        # Test the case when using a Coverage with a subset
        coverage1 = Coverage("Temperature")
        case = Case(coverage1 > 50, self.color)
        axis1 = Axis("Lat", 53.08)
        axis2 = Axis("Long", 8.80)
        coverage1.set_subset(axis1, axis2)
        expected_str = "case ($c1[Lat(53.08), Long(8.8)] > 50)\n\t\treturn {red: 100; green: 150; blue: 200}"
        self.assertEqual(str(case), expected_str)
        

if __name__ == '__main__':
    unittest.main()

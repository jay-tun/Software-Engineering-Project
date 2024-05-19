import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('../src/wdc')
from wdc import Switch, Case, RGBColor, Coverage, Axis

class TestSwitch(unittest.TestCase):
    def setUp(self):
        # Initialize an RGBColor instance for testing
        self.default_color = RGBColor(0, 0, 0)

    def test_initialization(self):
        # Test initialization of Switch instance
        switch = Switch(self.default_color)
        self.assertEqual(switch.RGBColor, self.default_color)
        self.assertEqual(len(switch.cases), 0)

    def test_add_case(self):
        # Test adding a Case object to the Switch
        switch = Switch(self.default_color)

        # Add a case
        case1 = Case("temperature > 30", RGBColor(255, 0, 0))
        switch.add_case(case1)
        self.assertEqual(len(switch.cases), 1)
        self.assertEqual(switch.cases[0], case1)

        # Add another case
        case2 = Case("temperature < 10", RGBColor(0, 0, 255))
        switch.add_case(case2)
        self.assertEqual(len(switch.cases), 2)
        self.assertEqual(switch.cases[1], case2)

    def test_string_representation(self):
        # Test string representation of Switch instance
        switch = Switch(self.default_color)
        case1 = Case("temperature > 30", RGBColor(255, 0, 0))
        switch.add_case(case1)
        case2 = Case("temperature < 10", RGBColor(0, 0, 255))
        switch.add_case(case2)

        expected_str = ("switch\n"
                        f"\t{str(case1)}\n"
                        f"\t{str(case2)}\n"
                        f"\tdefault return {self.default_color}")
        self.assertEqual(str(switch), expected_str)
        
    def test_with_coverages(self):
        # Test adding cases with Coverages to the Switch
        switch = Switch(self.default_color)

        # Create Coverage instances
        coverage1 = Coverage("Temperature")
        coverage2 = Coverage("Humidity")

        # Add cases with Coverages
        case1 = Case(coverage1 > 30, RGBColor(255, 0, 0))
        switch.add_case(case1)
        case2 = Case(coverage2 < 10, RGBColor(0, 0, 255))
        switch.add_case(case2)

        expected_str = ("switch\n"
                        f"\t{str(case1)}\n"
                        f"\t{str(case2)}\n"
                        f"\tdefault return {self.default_color}")
        self.assertEqual(str(switch), expected_str)

    def test_with_coverages_and_subsets(self):
        # Test adding cases with Coverages and subsets to the Switch
        switch = Switch(self.default_color)

        # Create Coverage instances with subsets
        coverage1 = Coverage("Temperature")
        axis1 = Axis("Lat", 53.08)
        axis2 = Axis("Long", 8.80)
        coverage1.set_subset(axis1, axis2)

        coverage2 = Coverage("Humidity")
        axis3 = Axis("Time", 2022)
        coverage2.set_subset(axis3)

        # Add cases with Coverages and subsets
        case1 = Case(coverage1 - coverage2 > 20, RGBColor(255, 0, 0))
        switch.add_case(case1)
        case2 = Case(coverage1 + coverage2 < 100, RGBColor(0, 255, 0))
        switch.add_case(case2)

        expected_str = ("switch\n"
                        f"\t{str(case1)}\n"
                        f"\t{str(case2)}\n"
                        f"\tdefault return {self.default_color}")
        self.assertEqual(str(switch), expected_str)

if __name__ == '__main__':
    unittest.main()
import unittest
from unittest.mock import patch, MagicMock
import sys
sys.path.append('../src/wdc')
import numpy as np  # Import NumPy for image comparison
from PIL import Image  # Import PIL for image handling
from wdc import Query, DatabaseConnection, Coverage, Axis, BinaryOperation, Case, Switch, RGBColor, CoverageConstructor

class TestQuery(unittest.TestCase):
    def setUp(self):
        # Initialize a mock DatabaseConnection for testing
        self.dbc = DatabaseConnection("https://ows.rasdaman.org/rasdaman/ows")
        
        # Reset coverage counter for each test
        Coverage.coverage_counter = 1

    def test_add_coverage(self):
        # Test adding a coverage to the query
        query = Query(self.dbc)
        coverage = Coverage("Temperature")
        query.add_coverage(coverage)
        self.assertEqual(query.coverages, [coverage])
        
    def test_add_three_coverages(self):
        # Test adding three coverages to the query
        query = Query(self.dbc)
        coverage1 = Coverage("Temperature")
        coverage2 = Coverage("Pressure")
        coverage3 = Coverage("Humidity")
        query.add_coverage(coverage1)
        query.add_coverage(coverage2)
        query.add_coverage(coverage3)
        self.assertEqual(query.coverages, [coverage1, coverage2, coverage3])

    def test_set_return(self):
        # Test setting the return type and value
        query = Query(self.dbc)
        query.set_return('CSV', 'data')
        self.assertEqual(query.return_type, 'CSV')
        self.assertEqual(query.return_value, 'data')

    def test_set_operation(self):
        # Test setting the operation
        query = Query(self.dbc)
        query.set_operation('max')
        self.assertEqual(query.operation, 'max')

    def test_set_count_condition(self):
        # Test setting the count condition
        query = Query(self.dbc)
        query.set_count_condition('temperature > 30')
        self.assertEqual(query.count_condition, 'temperature > 30')

    def test_set_switch(self):
        # Test setting the switch statement
        query = Query(self.dbc)
        switch = Switch(RGBColor(255, 0, 0))
        query.set_switch(switch)
        self.assertEqual(query.Switch, switch)

    """
    Tests for query generation
    """
    
    def test_basic_query(self):
        # Test for the most basic query
        coverage1 = Coverage("AvgLandTemp")
        query = Query(self.dbc)
        query.add_coverage(coverage1)
        query.set_return('CSV', 1)
        generated_query = query.generate_query(coverage1)
        
        self.assertIn('for $c1 in (AvgLandTemp)\nreturn 1', generated_query)
        
    def test_selecting_value_query(self):
        # Test for selecting a single value
        coverage1 = Coverage("AvgLandTemp")
        lat = Axis("Lat" , 53.08)
        long = Axis("Long", 8.80)
        ansi = Axis("ansi", '"2014-07"')
        coverage1.set_subset(lat, long, ansi)
        query = Query(self.dbc)
        query.add_coverage(coverage1)
        generated_query = query.generate_query(coverage1)
        
        self.assertIn('for $c1 in (AvgLandTemp)\nreturn ($c1[Lat(53.08), Long(8.8), ansi("2014-07")])', generated_query)
        
    def test_3d_1d_subset_query(self):
        # Test for 3D -> 1D subset
        coverage1 = Coverage("AvgLandTemp")
        lat = Axis("Lat" , 53.08)
        long = Axis("Long", 8.80)
        ansi = Axis("ansi", '"2014-01"', '"2014-12"')
        coverage1.set_subset(lat, long, ansi)
        query = Query(self.dbc)
        query.add_coverage(coverage1)
        query.set_operation('encode')
        query.set_return('CSV')
        generated_query = query.generate_query(coverage1)
        
        self.assertIn('for $c1 in (AvgLandTemp)\nreturn encode($c1[Lat(53.08), Long(8.8), ansi("2014-01":"2014-12")], "text/csv")', generated_query)

    def test_3d_2d_subset_query(self):
        # Test for 3D -> 2D subset
        coverage1 = Coverage("AvgTemperatureColorScaled")
        ansi = Axis("ansi", '"2014-07"')
        coverage1.set_subset(ansi)
        query = Query(self.dbc)
        query.add_coverage(coverage1)
        query.set_operation('encode')
        query.set_return('PNG')
        generated_query = query.generate_query(coverage1)
        
        self.assertIn('for $c1 in (AvgTemperatureColorScaled)\nreturn encode($c1[ansi("2014-07")], "image/png")', generated_query)

    def test_celsius_to_kelvin(self):
        # Celsius to kelvin
        coverage1 = Coverage("AvgLandTemp")
        lat = Axis("Lat" , 53.08)
        long = Axis("Long", 8.80)
        ansi = Axis("ansi", '"2014-01"', '"2014-12"')
        coverage1.set_subset(lat, long, ansi)
        query = Query(self.dbc)
        query.add_coverage(coverage1)
        query.set_operation('encode')
        query.set_return('CSV')
        generated_query = query.generate_query(coverage1 + 273.15)
        
        self.assertIn('for $c1 in (AvgLandTemp)\nreturn encode(($c1[Lat(53.08), Long(8.8), ansi("2014-01":"2014-12")] + 273.15), "text/csv")', generated_query)

    def test_min(self):
        # Test min
        coverage1 = Coverage("AvgLandTemp")
        lat = Axis("Lat" , 53.08)
        long = Axis("Long", 8.80)
        ansi = Axis("ansi", '"2014-01"', '"2014-12"')
        coverage1.set_subset(lat, long, ansi)
        query = Query(self.dbc)
        query.add_coverage(coverage1)
        query.set_operation('min')
        generated_query = query.generate_query(coverage1)
        
        self.assertIn('for $c1 in (AvgLandTemp)\nreturn min($c1[Lat(53.08), Long(8.8), ansi("2014-01":"2014-12")])', generated_query)

    def test_max(self):
        # Test max
        coverage1 = Coverage("AvgLandTemp")
        lat = Axis("Lat" , 53.08)
        long = Axis("Long", 8.80)
        ansi = Axis("ansi", '"2014-01"', '"2014-12"')
        coverage1.set_subset(lat, long, ansi)
        query = Query(self.dbc)
        query.add_coverage(coverage1)
        query.set_operation('max')
        generated_query = query.generate_query(coverage1)
        
        self.assertIn('for $c1 in (AvgLandTemp)\nreturn max($c1[Lat(53.08), Long(8.8), ansi("2014-01":"2014-12")])', generated_query)

    def test_avg(self):
        # Test avg
        coverage1 = Coverage("AvgLandTemp")
        lat = Axis("Lat" , 53.08)
        long = Axis("Long", 8.80)
        ansi = Axis("ansi", '"2014-01"', '"2014-12"')
        coverage1.set_subset(lat, long, ansi)
        query = Query(self.dbc)
        query.add_coverage(coverage1)
        query.set_operation('avg')
        generated_query = query.generate_query(coverage1)
        
        self.assertIn('for $c1 in (AvgLandTemp)\nreturn avg($c1[Lat(53.08), Long(8.8), ansi("2014-01":"2014-12")])', generated_query)

    def test_count(self):
        # Test when is temp more than 15
        coverage1 = Coverage("AvgLandTemp")
        lat = Axis("Lat" , 53.08)
        long = Axis("Long", 8.80)
        ansi = Axis("ansi", '"2014-01"', '"2014-12"')
        coverage1.set_subset(lat, long, ansi)
        query = Query(self.dbc)
        query.add_coverage(coverage1)
        query.set_operation('count')
        query.set_count_condition('> 15')
        generated_query = query.generate_query(coverage1)
        
        self.assertIn('for $c1 in (AvgLandTemp)\nreturn count($c1[Lat(53.08), Long(8.8), ansi("2014-01":"2014-12")] > 15)', generated_query)
        
    def test_switch(self):
        # Test switch / color coding
        coverage1 = Coverage("AvgLandTemp")
        ansi = Axis("ansi", '"2014-07"')
        lat = Axis("Lat", 35, 75)
        long = Axis("Long", -20, 40)
        coverage1.set_subset(lat, long, ansi)
        DefaultColor = RGBColor(255, 0, 0)
        SwitchStatement = Switch(DefaultColor)
        Color1 = RGBColor(255, 255, 255)
        Color2 = RGBColor(0, 0, 255)
        Color3 = RGBColor(255, 255, 0)
        Color4 = RGBColor(255, 140, 0)
        Case1 = Case(coverage1 == 99999, Color1)
        Case2 = Case(18 > coverage1, Color2)
        Case3 = Case(23 > coverage1, Color3)
        Case4 = Case(30 > coverage1, Color4)
        SwitchStatement.add_case(Case1)
        SwitchStatement.add_case(Case2)
        SwitchStatement.add_case(Case3)
        SwitchStatement.add_case(Case4)
        query = Query(self.dbc)
        query.add_coverage(coverage1)
        query.set_operation('colorcoding')
        query.set_return('PNG')
        query.set_switch(SwitchStatement)
        generated_query = query.generate_query(coverage1)
        expected_query = '''for $c1 in (AvgLandTemp)\n return encode(\n    switch\n\tcase ($c1[Lat(35:75), Long(-20:40), ansi("2014-07")] = 99999)\n\t\treturn {red: 255; green: 255; blue: 255}\n\tcase ($c1[Lat(35:75), Long(-20:40), ansi("2014-07")] < 18)\n\t\treturn {red: 0; green: 0; blue: 255}\n\tcase ($c1[Lat(35:75), Long(-20:40), ansi("2014-07")] < 23)\n\t\treturn {red: 255; green: 255; blue: 0}\n\tcase ($c1[Lat(35:75), Long(-20:40), ansi("2014-07")] < 30)\n\t\treturn {red: 255; green: 140; blue: 0}\n\tdefault return {red: 255; green: 0; blue: 0}\n\t, "image/png")'''

        self.assertIn(expected_query, generated_query)


if __name__ == '__main__':
    unittest.main()
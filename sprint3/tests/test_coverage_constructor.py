import unittest
import sys
sys.path.append('../src/wdc')
from wdc import CoverageConstructor

class TestCoverageConstructor(unittest.TestCase):
    
    def test_create_coverage_default(self):
        constructor = CoverageConstructor("myCoverage1", "$x + $y")
        
        self.assertEqual(constructor.new_name, "myCoverage1")
        self.assertEqual(constructor.__str__(), "coverage myCoverage1 over $x x(0:200), $y y(0:200) values $x + $y")
        
    def test_create_coverage_new(self):
        constructor = CoverageConstructor("myCoverage1", "$x + $y", (0, 150), (0, 150))
        
        self.assertEqual(constructor.new_name, "myCoverage1")
        self.assertEqual(constructor.__str__(), "coverage myCoverage1 over $x x(0:150), $y y(0:150) values $x + $y")
    def test_set_axis(self):
        constructor = CoverageConstructor("myCoverage1", "$x + $y", (0, 150), (0, 150))
        constructor.set_axis((50, 80), (20, 30))
        self.assertEqual(constructor.__str__(), "coverage myCoverage1 over $x x(50:80), $y y(20:30) values $x + $y")

if __name__ == '__main__':
    unittest.main()
import unittest
import pandas as pd
import numpy as np
from kkexpr.expr_functions.expr_binary import greater, less, cross_up, cross_down

class TestBinaryFunctions(unittest.TestCase):
    def setUp(self):
        self.dates = pd.date_range('2022-01-01', '2022-01-10')
        self.series1 = pd.Series(np.random.randn(10), index=self.dates)
        self.series2 = pd.Series(np.random.randn(10), index=self.dates)
        
    def test_greater(self):
        result = greater(self.series1, self.series2)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.series1))
        
    def test_less(self):
        result = less(self.series1, self.series2)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.series1))
        
    def test_cross_up(self):
        # Create specific test case for cross up
        s1 = pd.Series([1, 2, 3, 2, 3], index=self.dates[:5])
        s2 = pd.Series([2, 2, 2, 2, 2], index=self.dates[:5])
        result = cross_up(s1, s2)
        self.assertTrue(result.iloc[2])  # Should cross up at index 2
        
    def test_cross_down(self):
        # Create specific test case for cross down
        s1 = pd.Series([3, 2, 1, 2, 1], index=self.dates[:5])
        s2 = pd.Series([2, 2, 2, 2, 2], index=self.dates[:5])
        result = cross_down(s1, s2)
        self.assertTrue(result.iloc[2])  # Should cross down at index 2

if __name__ == '__main__':
    unittest.main() 
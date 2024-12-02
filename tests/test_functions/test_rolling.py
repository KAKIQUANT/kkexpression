import unittest
import pandas as pd
import numpy as np
from kkexpr.expr_functions.expr_binary_rolling import correlation, covariance
from kkexpr.expr_functions.expr_unary_rolling import ma, std, ts_max, ts_min

class TestRollingFunctions(unittest.TestCase):
    def setUp(self):
        self.dates = pd.date_range('2022-01-01', '2022-01-31')
        self.series = pd.Series(np.random.randn(31), index=self.dates)
        self.series2 = pd.Series(np.random.randn(31), index=self.dates)
        
    def test_ma(self):
        result = ma(self.series, 5)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.series))
        # First 4 values should be NaN
        self.assertTrue(np.isnan(result.iloc[:4]).all())
        
    def test_std(self):
        result = std(self.series, 5)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.series))
        self.assertTrue(np.isnan(result.iloc[:4]).all())
        
    def test_correlation(self):
        result = correlation(self.series, self.series2, 10)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.series))
        self.assertTrue(np.isnan(result.iloc[:9]).all())
        
    def test_ts_max(self):
        result = ts_max(self.series, 5)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.series))
        self.assertTrue(np.isnan(result.iloc[:4]).all())
        
    def test_ts_min(self):
        result = ts_min(self.series, 5)
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.series))
        self.assertTrue(np.isnan(result.iloc[:4]).all())

if __name__ == '__main__':
    unittest.main() 
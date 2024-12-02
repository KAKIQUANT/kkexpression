import unittest
import pandas as pd
import numpy as np
from tests.test_utils import create_test_data
from kkexpr.expr.functions import (
    ma, std, correlation, cross_up, cross_down,
    bbands_up, ta_atr, ta_obv
)

class TestFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dates = pd.date_range('2022-01-01', '2022-01-31')
        cls.symbols = ['000001.XSHE']
        cls.data = create_test_data(cls.dates, cls.symbols)
        
    def test_rolling_functions(self):
        """Test rolling window functions."""
        close = self.data['close']
        
        # Test MA
        result = ma(close, 5)
        self.assertIsInstance(result, pd.Series)
        self.assertTrue(np.isnan(result.iloc[:4]).all())
        
        # Test STD
        result = std(close, 5)
        self.assertIsInstance(result, pd.Series)
        self.assertTrue(np.isnan(result.iloc[:4]).all())
        
        # Test correlation
        result = correlation(close, self.data['volume'], 10)
        self.assertIsInstance(result, pd.Series)
        self.assertTrue(np.isnan(result.iloc[:9]).all())

    def test_binary_functions(self):
        """Test binary functions."""
        s1 = pd.Series([1, 2, 3, 2, 3], index=self.dates[:5])
        s2 = pd.Series([2, 2, 2, 2, 2], index=self.dates[:5])
        
        # Test cross_up
        result = cross_up(s1, s2)
        self.assertTrue(result.iloc[2])
        
        # Test cross_down
        s1 = pd.Series([3, 2, 1, 2, 1], index=self.dates[:5])
        result = cross_down(s1, s2)
        self.assertTrue(result.iloc[2])

    def test_technical_functions(self):
        """Test technical indicators."""
        close = self.data['close']
        high = self.data['high']
        low = self.data['low']
        volume = self.data['volume']
        
        # Test Bollinger Bands
        result = bbands_up(close)
        self.assertIsInstance(result, pd.Series)
        
        # Test ATR
        result = ta_atr(high, low, close)
        self.assertIsInstance(result, pd.Series)
        
        # Test OBV
        result = ta_obv(close, volume)
        self.assertIsInstance(result, pd.Series)

if __name__ == '__main__':
    unittest.main() 
import unittest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from kkexpr.expr.functions.rolling import (
    correlation, covariance, ma, std, ts_max, ts_min, ts_rank,
    sum, shift, roc, zscore, scale, decay_linear, slope_pair,
    ts_corr, RSRS, sign, ta_obv
)

class TestRollingFunctions(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create test data
        dates = pd.date_range(start='2024-01-01', periods=60, freq='D')
        symbols = ['CL', 'GDAXI', 'GOLD', 'HSI', 'N225']
        
        # Create multi-index data with realistic price movements
        data = []
        for i, symbol in enumerate(symbols):
            np.random.seed(42 + i)  # Different seed for each symbol
            
            # Generate realistic price series
            returns = np.random.normal(0.0001, 0.02, size=60)  # Daily returns
            price = 100 * np.exp(np.cumsum(returns))  # Log-normal prices
            
            series = pd.Series(
                price,
                index=pd.MultiIndex.from_product(
                    [[symbol], dates],
                    names=['symbol', 'date']
                )
            )
            data.append(series)
        
        cls.series = pd.concat(data)
        
        # Create correlated series for testing
        noise = np.random.randn(len(cls.series)) * 0.1
        cls.series2 = cls.series * 1.5 + noise  # Correlated series
        
        # Create volume series
        cls.volume = pd.Series(
            np.abs(np.random.normal(1e6, 2e5, size=len(cls.series))),
            index=cls.series.index
        )

    def test_correlation(self):
        result = correlation(self.series, self.series2, periods=10)
        self.assertIsInstance(result, pd.Series)
        self.assertTrue(result.notna().any())
        # First 9 values should be NaN for each symbol
        for symbol in ['CL', 'GDAXI', 'GOLD', 'HSI', 'N225']:
            symbol_data = result.xs(symbol, level='symbol')
            self.assertTrue(symbol_data.iloc[:9].isna().all())
        # Correlation should be between -1 and 1
        self.assertTrue((result.dropna() >= -1).all() and (result.dropna() <= 1).all())

    def test_ma(self):
        result = ma(self.series, periods=5)
        self.assertIsInstance(result, pd.Series)
        # Test for each symbol
        for symbol in ['CL', 'GDAXI', 'GOLD', 'HSI', 'N225']:
            symbol_data = result.xs(symbol, level='symbol')
            symbol_input = self.series.xs(symbol, level='symbol')
            # First 4 values should be NaN
            self.assertTrue(symbol_data.iloc[:4].isna().all())
            # Test specific value
            expected = symbol_input.iloc[:5].mean()
            self.assertAlmostEqual(symbol_data.iloc[4], expected)

    def test_ts_rank(self):
        result = ts_rank(self.series, periods=5)
        self.assertIsInstance(result, pd.Series)
        # Test for each symbol
        for symbol in ['CL', 'GDAXI', 'GOLD', 'HSI', 'N225']:
            symbol_data = result.xs(symbol, level='symbol')
            # Values should be between 0 and 1
            valid_data = symbol_data.dropna()
            self.assertTrue((valid_data >= 0).all() and (valid_data <= 1).all())

    def test_ta_obv(self):
        result = ta_obv(self.series, self.volume)
        self.assertIsInstance(result, pd.Series)
        # Test for each symbol
        for symbol in ['CL', 'GDAXI', 'GOLD', 'HSI', 'N225']:
            symbol_data = result.xs(symbol, level='symbol')
            symbol_price = self.series.xs(symbol, level='symbol')
            symbol_volume = self.volume.xs(symbol, level='symbol')
            
            # Manual OBV calculation
            sign = np.where(symbol_price > symbol_price.shift(1), 1, 
                          np.where(symbol_price < symbol_price.shift(1), -1, 0))
            expected = (sign * symbol_volume).cumsum()
            pd.testing.assert_series_equal(
                symbol_data, 
                expected, 
                check_dtype=False
            )

    def test_scale(self):
        result = scale(self.series, a=1.0)
        self.assertIsInstance(result, pd.Series)
        # Test for each symbol
        for symbol in ['CL', 'GDAXI', 'GOLD', 'HSI', 'N225']:
            symbol_data = result.xs(symbol, level='symbol')
            # Sum of absolute values should be close to a
            self.assertAlmostEqual(np.abs(symbol_data).sum(), 1.0, places=5)

    def test_decay_linear(self):
        result = decay_linear(self.series, window=5)
        self.assertIsInstance(result, pd.Series)
        # Test for each symbol
        for symbol in ['CL', 'GDAXI', 'GOLD', 'HSI', 'N225']:
            symbol_data = result.xs(symbol, level='symbol')
            symbol_input = self.series.xs(symbol, level='symbol')
            
            # First 4 values should be NaN
            self.assertTrue(symbol_data.iloc[:4].isna().all())
            
            # Test decay calculation
            window = symbol_input.iloc[:5]
            weights = np.arange(1, 6)
            expected = np.sum(window * weights) / np.sum(weights)
            self.assertAlmostEqual(symbol_data.iloc[4], expected, places=5)

    def test_RSRS(self):
        # Create high and low series with realistic spread
        spread = self.series * 0.02  # 2% spread
        high = self.series + spread/2
        low = self.series - spread/2
        
        result = RSRS(high, low, N=18)
        self.assertIsInstance(result, pd.Series)
        # Test for each symbol
        for symbol in ['CL', 'GDAXI', 'GOLD', 'HSI', 'N225']:
            symbol_data = result.xs(symbol, level='symbol')
            # First 17 values should be NaN
            self.assertTrue(symbol_data.iloc[:17].isna().all())
            # Beta should typically be positive for trending data
            self.assertTrue((symbol_data.dropna() > 0).mean() > 0.5)

if __name__ == '__main__':
    unittest.main() 
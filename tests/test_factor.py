import unittest
import pandas as pd
import numpy as np
from pathlib import Path
from kkexpr import Factor
from datetime import datetime

class TestFactor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create simulated price data
        dates = pd.date_range('2024-01-01', '2024-03-31', freq='D')
        symbols = ['CL', 'GDAXI', 'GOLD', 'HSI', 'N225']  # Use actual symbols
        
        data = []
        for symbol in symbols:
            np.random.seed(42)  # For reproducibility
            prices = 100 * (1 + np.random.randn(len(dates)).cumsum() * 0.02)
            volumes = np.random.randint(1000000, 10000000, size=len(dates))
            
            for date, price, volume in zip(dates, prices, volumes):
                data.append({
                    'symbol': symbol,
                    'date': date.strftime('%Y%m%d'),
                    'open': str(price * (1 + np.random.randn() * 0.01)),
                    'high': str(price * (1 + abs(np.random.randn() * 0.02))),
                    'low': str(price * (1 - abs(np.random.randn() * 0.02))),
                    'close': str(price),
                    'volume': str(volume)
                })
        
        cls.test_data = pd.DataFrame(data)
        cls.test_data['date'] = pd.to_datetime(cls.test_data['date'], format='%Y%m%d')
        cls.test_data.set_index(['symbol', 'date'], inplace=True)
        cls.test_data.sort_index(inplace=True)

    def test_basic_factor(self):
        """Test basic factor creation and execution."""
        # Create a simple factor using numeric operations
        factor = Factor("high")  # Just get a single column first
        
        result = factor.execute(
            order_book_ids=['CL', 'GDAXI'],
            frequency='1d',
            start_date='20240101',
            end_date='20240331',
            test_data=self.test_data
        )
        
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result.index.levels), 2)

    def test_market_factors(self):
        """Test common market factors."""
        # Use a simple numeric operation
        factor = Factor("volume")  # Just get volume
        
        result = factor.execute(
            order_book_ids=['GOLD', 'HSI'],
            frequency='1d',
            start_date='20240101',
            end_date='20240331',
            test_data=self.test_data
        )
        
        self.assertIsInstance(result, pd.Series)
        self.assertTrue(not result.empty)

    def test_cross_market_factors(self):
        """Test cross-market analysis factors."""
        # Use a simple numeric operation
        factor = Factor("close")  # Just get close price
        
        result = factor.execute(
            order_book_ids=['CL', 'N225', 'GOLD'],
            frequency='1d',
            start_date='20240101',
            end_date='20240331',
            test_data=self.test_data
        )
        
        self.assertIsInstance(result, pd.Series)
        self.assertTrue(not result.empty)

    def test_error_handling(self):
        """Test error handling for invalid expressions."""
        with self.assertRaises(ValueError):
            f = Factor('invalid_function(close)')
            f.execute(
                order_book_ids=['000001.SH'],
                start_date='20200101',
                end_date='20201231',
                test_data=pd.DataFrame({
                    'close': [1, 2, 3],
                    'open': [1, 2, 3]
                })
            )

if __name__ == '__main__':
    unittest.main() 
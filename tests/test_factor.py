import unittest
import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
from unittest.mock import patch
from tests.test_utils import create_test_data, mock_get_price

# Patch kkdatac before importing Factor
with patch('kkexpr.core.factor.get_price', mock_get_price):
    from kkexpr.core import Factor

class TestFactor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.dates = pd.date_range('2022-01-01', '2022-12-31')
        # Use real market symbols
        cls.symbols = ['CL', 'GDAXI', 'GOLD', 'HSI', 'N225', '^NDX', '^TNX']
        cls.data = create_test_data(cls.dates, cls.symbols)
        cls.data = cls.data.sort_index()

    def test_basic_factor(self):
        """Test basic factor creation and execution."""
        factor = Factor('close')
        result = factor.execute(
            order_book_ids=self.symbols[:3],  # Test with subset
            frequency='1d',
            start_date='20220101',
            end_date='20221231'
        )
        self.assertIsInstance(result, pd.Series)
        self.assertEqual(len(result), len(self.dates) * 3)

    def test_market_factors(self):
        """Test common market factors."""
        factors = {
            'daily_return': 'close/shift(close,1) - 1',
            'volatility': 'std(close/shift(close,1)-1, 20)',
            'momentum': 'close/shift(close,20) - 1',
            'volume_price_impact': 'correlation(abs(close/shift(close,1)-1), volume, 20)',
            'trend': 'ma(close,20)/ma(close,60) - 1'
        }
        
        for name, expr in factors.items():
            factor = Factor(expr)
            result = factor.execute(
                order_book_ids=self.symbols,
                frequency='1d',
                start_date='20220101',
                end_date='20221231'
            )
            self.assertIsInstance(result, pd.Series)

    def test_cross_market_factors(self):
        """Test cross-market analysis factors."""
        # Test correlation between Gold and Treasury yields
        factor = Factor('correlation(close, shift(close,1), 20)')
        result = factor.execute(
            order_book_ids=['GOLD', '^TNX'],
            frequency='1d',
            start_date='20220101',
            end_date='20221231'
        )
        self.assertIsInstance(result, pd.Series)

    def test_error_handling(self):
        """Test error handling for invalid expressions."""
        invalid_expressions = [
            'invalid_func(close)',
            'ma()',  # Missing arguments
            'correlation(close)',  # Insufficient arguments
            'close ++ open',  # Invalid operator
            'log()'  # Missing argument
        ]
        
        for expr in invalid_expressions:
            try:
                factor = Factor(expr)
                with self.assertRaises((ValueError, TypeError, SyntaxError)):
                    factor.execute(
                        order_book_ids=self.symbols,
                        frequency='1d',
                        start_date='20220101',
                        end_date='20221231'
                    )
            except (ValueError, TypeError, SyntaxError):
                pass

if __name__ == '__main__':
    unittest.main() 
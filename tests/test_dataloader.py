import unittest
import pandas as pd
import numpy as np
from pathlib import Path
from tests.test_utils import create_test_data, setup_test_data_dir
from kkexpr.data.loader import CSVDataloader

class TestDataloader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path(__file__).parent
        cls.paths = setup_test_data_dir(cls.test_dir)
        
        cls.dates = pd.date_range('2022-01-01', '2022-12-31')
        cls.symbols = ['CL', 'GDAXI', 'GOLD', 'HSI', 'N225', '^NDX', '^TNX']
        
        data = create_test_data(cls.dates, cls.symbols)
        for symbol in cls.symbols:
            symbol_data = data.loc[symbol].reset_index(level=0, drop=True)
            symbol_data.to_csv(cls.paths['quotes'] / f'{symbol}.csv')

    def test_basic_loading(self):
        """Test basic data loading."""
        loader = CSVDataloader(
            path=self.paths['quotes'],
            symbols=self.symbols[:3],
            start_date='20220101',
            end_date='20221231'
        )
        
        df = loader.load()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertTrue(all(col in df.columns for col in ['open', 'high', 'low', 'close', 'volume']))
        self.assertEqual(len(df), len(self.dates) * 3)
        self.assertTrue(isinstance(df.index, pd.MultiIndex))
        
    def test_expression_loading(self):
        """Test loading with expressions."""
        loader = CSVDataloader(
            path=self.paths['quotes'],
            symbols=self.symbols
        )
        
        fields = [
            'close/open - 1',  # Simple arithmetic
            'close/shift(close, 1) - 1',  # Returns
            'close/mean(close, 5) - 1',  # Normalized price
            'volume/mean(volume, 5) - 1'  # Volume ratio
        ]
        names = ['returns', 'daily_ret', 'norm_price', 'vol_ratio']
        
        df = loader.load(fields=fields, names=names)
        self.assertTrue(all(col in df.columns for col in names))

    def test_cross_market_loading(self):
        """Test loading data for cross-market analysis."""
        loader = CSVDataloader(
            path=self.paths['quotes'],
            symbols=['GOLD', '^TNX'],
            start_date='20220101',
            end_date='20221231'
        )
        
        fields = [
            'correlation(close, shift(close, 1), 20)',
            'std(close/shift(close,1)-1, 20)'
        ]
        names = ['auto_corr', 'volatility']
        
        df = loader.load(fields=fields, names=names)
        self.assertTrue(all(col in df.columns for col in names))
        self.assertEqual(len(df.index.levels[0]), 2)

    @classmethod
    def tearDownClass(cls):
        # Clean up test files
        import shutil
        shutil.rmtree(cls.paths['root'])

if __name__ == '__main__':
    unittest.main() 
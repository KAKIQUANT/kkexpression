import unittest
import pandas as pd
import numpy as np
from pathlib import Path
from tests.test_utils import create_test_data, setup_test_data_dir
from kkexpr import CSVDataloader

class TestDataloader(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = Path(__file__).parent
        cls.paths = setup_test_data_dir(cls.test_dir)
        
        # Get the actual dates from one of the files
        sample_data = pd.read_csv(cls.paths['quotes'] / 'HSI.csv')
        cls.dates = pd.to_datetime(sample_data['date'])
        cls.symbols = ['CL', 'GDAXI', 'GOLD', 'HSI', 'N225']

    def test_basic_loading(self):
        """Test basic data loading."""
        loader = CSVDataloader(
            path=self.paths['quotes'],
            symbols=['CL', 'GDAXI', 'GOLD'],
            start_date='20240101',
            end_date='20240331'
        )
        
        df = loader.load()
        self.assertIsInstance(df, pd.DataFrame)
        expected_columns = ['open', 'high', 'low', 'close', 'volume']
        self.assertTrue(all(col in df.columns for col in expected_columns))
        self.assertTrue(isinstance(df.index, pd.MultiIndex))
        for col in expected_columns:
            self.assertTrue(df[col].dtype == object or df[col].dtype == str)

    def test_column_loading(self):
        """Test loading specific columns."""
        loader = CSVDataloader(
            path=self.paths['quotes'],
            symbols=['CL', 'GDAXI', 'GOLD', 'HSI', 'N225'],
            start_date='20240101',
            end_date=None
        )
        
        fields = ['open', 'high', 'low']
        df = loader.load(fields=fields)
        self.assertTrue(all(col in df.columns for col in fields))
        for col in fields:
            self.assertTrue(df[col].dtype == object or df[col].dtype == str)

    def test_multi_symbol_loading(self):
        """Test loading data for multiple symbols."""
        loader = CSVDataloader(
            path=self.paths['quotes'],
            symbols=['GOLD', 'N225'],
            start_date='20240101',
            end_date='20240331'
        )
        
        df = loader.load()
        expected_columns = ['open', 'high', 'low', 'close', 'volume']
        self.assertTrue(all(col in df.columns for col in expected_columns))
        self.assertEqual(len(df.index.levels[0]), 2)
        for col in expected_columns:
            self.assertTrue(df[col].dtype == object or df[col].dtype == str)

if __name__ == '__main__':
    unittest.main() 
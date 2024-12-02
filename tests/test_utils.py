import pandas as pd
import numpy as np
from pathlib import Path
from typing import List, Dict
from unittest.mock import MagicMock
from datetime import datetime

def create_test_data(dates: pd.DatetimeIndex, symbols: List[str]) -> pd.DataFrame:
    """Create test data for multiple symbols."""
    data = []
    for symbol in symbols:
        df = pd.DataFrame({
            'open': np.random.randn(len(dates)),
            'high': np.random.randn(len(dates)),
            'low': np.random.randn(len(dates)),
            'close': np.random.randn(len(dates)),
            'volume': np.abs(np.random.randn(len(dates))),
            'symbol': symbol
        }, index=dates)
        data.append(df)
    
    df = pd.concat(data)
    # Create MultiIndex correctly
    df = df.set_index('symbol', append=True)
    df = df.swaplevel()  # Make symbol the first level
    df.index.names = ['symbol', 'date']
    return df.sort_index()

def setup_test_data_dir(base_path: Path) -> Dict[str, Path]:
    """Setup test data directory structure."""
    paths = {
        'root': base_path / 'test_data',
        'quotes': base_path / 'test_data' / 'quotes',
    }
    
    for path in paths.values():
        path.mkdir(parents=True, exist_ok=True)
        
    return paths

# Mock for kkdatac.get_price
def mock_get_price(order_book_ids, frequency, start_date, end_date):
    """Mock implementation of get_price."""
    if isinstance(start_date, datetime):
        start_date = start_date.strftime('%Y%m%d')
    if isinstance(end_date, datetime):
        end_date = end_date.strftime('%Y%m%d')
        
    dates = pd.date_range(start_date, end_date)
    df = create_test_data(dates, order_book_ids)
    return df

# Create mock module
mock_kkdatac = MagicMock()
mock_kkdatac.get_price = mock_get_price
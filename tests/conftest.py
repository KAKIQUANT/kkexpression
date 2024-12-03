import sys
from pathlib import Path
import pytest
import pandas as pd
import numpy as np

# Add project root to path for pytest
project_root = str(Path(__file__).parent.parent.absolute())
if project_root not in sys.path:
    sys.path.insert(0, project_root) 

@pytest.fixture
def sample_data():
    """Create sample price data for testing."""
    dates = pd.date_range('2020-01-01', '2020-12-31')
    symbols = ['000001.SH', '000002.SH', '000003.SH']
    
    # Create multi-index DataFrame
    index = pd.MultiIndex.from_product([symbols, dates], names=['symbol', 'date'])
    
    np.random.seed(42)
    data = pd.DataFrame({
        'close': np.random.randn(len(index)),
        'open': np.random.randn(len(index)),
        'high': np.random.randn(len(index)),
        'low': np.random.randn(len(index)),
        'volume': np.abs(np.random.randn(len(index))),
    }, index=index)
    
    return data

@pytest.fixture
def sample_returns(sample_data):
    """Create sample returns data."""
    return sample_data['close'].pct_change() 
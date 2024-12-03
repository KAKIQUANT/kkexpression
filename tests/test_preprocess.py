import pytest
import pandas as pd
import numpy as np
from kkexpr.core.preprocess import winsorize, standardize, neutralize

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    np.random.seed(42)
    return pd.DataFrame({
        'values': np.random.randn(1000),
        'group': np.random.choice(['A', 'B', 'C'], 1000),
        'style1': np.random.randn(1000),
        'style2': np.random.randn(1000)
    })

def test_winsorize(sample_data):
    """Test winsorization."""
    # Test MAD method
    result = winsorize(sample_data['values'], method='mad', n_std=3)
    assert isinstance(result, pd.Series)
    assert result.min() > sample_data['values'].min()
    assert result.max() < sample_data['values'].max()
    
    # Test STD method
    result = winsorize(sample_data['values'], method='std', n_std=3)
    assert isinstance(result, pd.Series)
    assert result.min() > sample_data['values'].min()
    assert result.max() < sample_data['values'].max()

def test_standardize(sample_data):
    """Test standardization."""
    result = standardize(sample_data['values'])
    assert isinstance(result, pd.Series)
    assert np.abs(result.mean()) < 1e-10
    assert np.abs(result.std() - 1) < 1e-10

def test_neutralize(sample_data):
    """Test neutralization."""
    # Test group neutralization
    result = neutralize(
        sample_data['values'],
        groups=sample_data['group']
    )
    assert isinstance(result, pd.Series)
    
    # Test with style factors
    result = neutralize(
        sample_data['values'],
        groups=sample_data['group'],
        style_factors=sample_data[['style1', 'style2']]
    )
    assert isinstance(result, pd.Series) 
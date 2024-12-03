import pytest
import pandas as pd
import numpy as np
from kkexpr.expr.functions import (
    greater, less, cross_up, cross_down,
    gt, lt, ge, le, eq, ne, max_, min_
)

@pytest.fixture
def sample_data():
    """Create sample data for testing."""
    dates = pd.date_range('2020-01-01', '2020-12-31')
    np.random.seed(42)
    data = pd.DataFrame({
        'a': np.random.randn(len(dates)),
        'b': np.random.randn(len(dates))
    }, index=dates)
    return data

def test_greater(sample_data):
    """Test greater function."""
    result = greater(sample_data['a'], sample_data['b'])
    assert isinstance(result, pd.Series)
    assert result.dtype == bool

def test_less(sample_data):
    """Test less function."""
    result = less(sample_data['a'], sample_data['b'])
    assert isinstance(result, pd.Series)
    assert result.dtype == bool

def test_cross_up(sample_data):
    """Test cross_up function."""
    result = cross_up(sample_data['a'], sample_data['b'])
    assert isinstance(result, pd.Series)
    assert result.dtype == bool

def test_cross_down(sample_data):
    """Test cross_down function."""
    result = cross_down(sample_data['a'], sample_data['b'])
    assert isinstance(result, pd.Series)
    assert result.dtype == bool

def test_comparison_operators(sample_data):
    """Test comparison operators."""
    operators = [gt, lt, ge, le, eq, ne]
    for op in operators:
        result = op(sample_data['a'], sample_data['b'])
        assert isinstance(result, pd.Series)
        assert result.dtype == bool

def test_max_min(sample_data):
    """Test max and min functions."""
    max_result = max_(sample_data['a'], sample_data['b'])
    assert isinstance(max_result, pd.Series)
    
    min_result = min_(sample_data['a'], sample_data['b'])
    assert isinstance(min_result, pd.Series)

def test_cross_up():
    """Test cross_up function with specific cases."""
    dates = pd.date_range('2020-01-01', '2020-01-05')
    
    # Case 1: Simple crossing
    s1 = pd.Series([1.0, 1.8, 2.2, 2.0, 3.0], index=dates)
    s2 = pd.Series([2.0, 2.0, 2.0, 2.0, 2.0], index=dates)
    result = cross_up(s1, s2)
    assert result.iloc[2], "Should detect crossing at index 2"
    assert not result.iloc[0], "Should not detect crossing at start"
    
    # Case 2: Multiple crossings
    s1 = pd.Series([1.0, 2.5, 1.5, 2.5, 1.5], index=dates)
    s2 = pd.Series([2.0, 2.0, 2.0, 2.0, 2.0], index=dates)
    result = cross_up(s1, s2)
    assert result.iloc[1], "Should detect first crossing"
    assert result.iloc[3], "Should detect second crossing"
    
    # Case 3: Touching but not crossing
    s1 = pd.Series([1.0, 2.0, 1.9, 2.0, 1.8], index=dates)
    s2 = pd.Series([2.0, 2.0, 2.0, 2.0, 2.0], index=dates)
    result = cross_up(s1, s2)
    assert not result.any(), "Should not detect crossing when only touching"
    
    # Case 4: String values
    s1 = pd.Series(['1.0', '1.8', '2.2', '2.0', '3.0'], index=dates)
    s2 = pd.Series(['2.0', '2.0', '2.0', '2.0', '2.0'], index=dates)
    result = cross_up(s1, s2)
    assert result.iloc[2], "Should handle string values correctly"

def test_cross_down():
    """Test cross_down function with specific cases."""
    dates = pd.date_range('2020-01-01', '2020-01-05')
    
    # Case 1: Simple crossing
    s1 = pd.Series([3.0, 2.2, 1.8, 2.0, 1.0], index=dates)
    s2 = pd.Series([2.0, 2.0, 2.0, 2.0, 2.0], index=dates)
    result = cross_down(s1, s2)
    assert result.iloc[2], "Should detect crossing at index 2"
    assert not result.iloc[0], "Should not detect crossing at start"
    
    # Case 2: Multiple crossings
    s1 = pd.Series([3.0, 1.5, 2.5, 1.5, 2.5], index=dates)
    s2 = pd.Series([2.0, 2.0, 2.0, 2.0, 2.0], index=dates)
    result = cross_down(s1, s2)
    assert result.iloc[1], "Should detect first crossing"
    assert result.iloc[3], "Should detect second crossing"
    
    # Case 3: Touching but not crossing
    s1 = pd.Series([3.0, 2.0, 2.1, 2.0, 2.2], index=dates)
    s2 = pd.Series([2.0, 2.0, 2.0, 2.0, 2.0], index=dates)
    result = cross_down(s1, s2)
    assert not result.any(), "Should not detect crossing when only touching" 
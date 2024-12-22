import pytest
import polars as pl
from kkexpr_rust import PyFactor

def test_simple_factor():
    # Create test data
    df = pl.DataFrame({
        'close': [100.0, 101.0, 99.0, 102.0, 98.0],
        'volume': [1000.0, 2000.0, 1500.0, 3000.0, 1200.0]
    })
    
    # Create and compute factor
    factor = PyFactor("MA(close, 3)")
    result = factor.compute(df)
    
    # Check result
    assert len(result) == len(df)
    assert result.dtypes[0] == pl.Float64

def test_arithmetic_factor():
    df = pl.DataFrame({
        'close': [100.0, 101.0, 99.0, 102.0, 98.0]
    })
    
    factor = PyFactor("close + 1")
    result = factor.compute(df)
    
    expected = df['close'] + 1
    assert (result == expected).all() 
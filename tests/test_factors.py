import pytest
import pandas as pd
import numpy as np
from datetime import datetime
from kkexpr import Factor
from kkexpr.core.analysis import FactorAnalysis
from kkexpr.core.preprocess import winsorize, standardize, neutralize

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

def test_basic_factor_creation():
    """Test basic factor creation."""
    f = Factor('close')
    assert str(f) == 'close'
    
    f = Factor('close/open')
    assert str(f) == 'close/open'

def test_factor_arithmetic():
    """Test factor arithmetic operations."""
    f1 = Factor('close')
    f2 = Factor('open')
    
    f3 = f1 + f2
    assert str(f3) == '(close + open)'
    
    f4 = f1 * f2
    assert str(f4) == '(close * open)'

def test_factor_execution(sample_data):
    """Test factor calculation execution."""
    f = Factor('close/open')
    result = f.execute(
        order_book_ids=['000001.SH'],
        start_date='20200101',
        end_date='20201231',
        test_data=sample_data
    )
    
    assert isinstance(result, pd.Series)
    assert not result.empty

def test_technical_operators(sample_data):
    """Test technical analysis operators."""
    # Test MA
    f = Factor('MA(close, 20)')
    result = f.execute(
        order_book_ids=['000001.SH'],
        start_date='20200101',
        end_date='20201231',
        test_data=sample_data
    )
    assert isinstance(result, pd.Series)
    
    # Test RSI
    f = Factor('RSI(close, 14)')
    result = f.execute(
        order_book_ids=['000001.SH'],
        start_date='20200101',
        end_date='20201231',
        test_data=sample_data
    )
    assert isinstance(result, pd.Series)

def test_preprocessing(sample_data):
    """Test factor preprocessing."""
    f = Factor('close/open')
    
    # Test winsorization
    f.winsorize(method='mad', n_std=3)
    result = f.execute(
        order_book_ids=['000001.SH'],
        start_date='20200101',
        end_date='20201231',
        test_data=sample_data
    )
    assert isinstance(result, pd.Series)
    
    # Test standardization
    f.standardize()
    result = f.execute(
        order_book_ids=['000001.SH'],
        start_date='20200101',
        end_date='20201231',
        test_data=sample_data
    )
    assert isinstance(result, pd.Series)

def test_factor_analysis(sample_data, sample_returns):
    """Test factor analysis functionality."""
    # Calculate factor values
    f = Factor('close/open')
    factor_data = f.execute(
        order_book_ids=['000001.SH'],
        start_date='20200101',
        end_date='20201231',
        test_data=sample_data
    )
    
    # Create analysis object
    analysis = FactorAnalysis(
        factor_data=factor_data,
        returns=sample_returns,
        quantiles=5,
        periods=[1, 5, 10]
    )
    
    # Test IC calculation
    ic = analysis.calc_ic()
    assert isinstance(ic, pd.DataFrame)
    
    # Test quantile returns
    q_returns = analysis.calc_quantile_returns()
    assert isinstance(q_returns, pd.DataFrame)
    
    # Test turnover calculation
    turnover = analysis.calc_turnover()
    assert isinstance(turnover, pd.Series)
    
    # Test IC stats
    ic_stats = analysis.calc_ic_stats()
    assert isinstance(ic_stats, pd.DataFrame)
    
    # Test quantile stats
    q_stats = analysis.calc_quantile_stats()
    assert isinstance(q_stats, pd.DataFrame)

def test_complex_expressions(sample_data):
    """Test complex factor expressions."""
    expressions = [
        'log(close/open)',
        'MA(close, 20) / MA(close, 60)',
        'CROSS_UP(close, MA(close, 20))',
        'RSI(close, 14) > 70',
        'correlation(close, volume, 20)',
        'ts_rank(volume, 20)',
        'ZSCORE(ROC(close, 20))'
    ]
    
    for expr in expressions:
        f = Factor(expr)
        result = f.execute(
            order_book_ids=['000001.SH'],
            start_date='20200101',
            end_date='20201231',
            test_data=sample_data
        )
        assert isinstance(result, (pd.Series, pd.DataFrame))
        assert not result.empty

def test_error_handling():
    """Test error handling."""
    # Test invalid expression
    with pytest.raises(ValueError):
        f = Factor('invalid_function(close)')
        f.execute(
            order_book_ids=['000001.SH'],
            start_date='20200101',
            end_date='20201231'
        ) 
import numpy as np
import pandas as pd
from typing import Union
from .utils import calc_by_symbol, calc_by_date

@calc_by_symbol
def correlation(left: pd.Series, right: pd.Series, periods: int = 20) -> pd.Series:
    """Calculate rolling correlation between two series."""
    res = left.rolling(window=periods).corr(right)
    mask = (
        np.isclose(left.rolling(periods).std(), 0, atol=2e-05) |
        np.isclose(right.rolling(periods).std(), 0, atol=2e-05)
    )
    res[mask] = np.nan
    return res

@calc_by_symbol
def covariance(left: pd.Series, right: pd.Series, periods: int = 10) -> pd.Series:
    """Calculate rolling covariance between two series."""
    return left.rolling(window=periods).cov(right)

@calc_by_symbol
def ma(series: pd.Series, periods: int = 20) -> pd.Series:
    """Calculate simple moving average."""
    return series.rolling(window=periods).mean()

@calc_by_symbol
def std(series: pd.Series, periods: int = 20) -> pd.Series:
    """Calculate rolling standard deviation."""
    return series.rolling(window=periods).std()

@calc_by_symbol
def ts_max(series: pd.Series, periods: int = 5) -> pd.Series:
    """Calculate rolling maximum."""
    return series.rolling(window=periods).max()

@calc_by_symbol
def ts_min(series: pd.Series, periods: int = 5) -> pd.Series:
    """Calculate rolling minimum."""
    return series.rolling(window=periods).min()

@calc_by_symbol
def ts_rank(series: pd.Series, periods: int = 9) -> pd.Series:
    """Calculate rolling rank."""
    return series.rolling(window=periods).rank(pct=True)

@calc_by_symbol
def sum(series: pd.Series, periods: int) -> pd.Series:
    """Calculate rolling sum."""
    result = series.rolling(periods).sum()
    result.name = f'sum_{periods}'
    return result

@calc_by_symbol
def shift(series: pd.Series, periods: int) -> pd.Series:
    """Shift series by given periods."""
    return series.shift(periods)

@calc_by_symbol
def roc(series: pd.Series, periods: int) -> pd.Series:
    """Calculate rate of change."""
    return series / shift(series, periods) - 1

@calc_by_symbol
def zscore(series: pd.Series, periods: int) -> pd.Series:
    """Calculate rolling z-score."""
    def _zscore(x):
        if len(x.dropna()) == 0:
            return np.nan
        return (x[-1] - x.mean()) / x.std() if x.std() != 0 else 0
    return series.rolling(window=periods).apply(_zscore)

@calc_by_symbol
def scale(series: pd.Series, a: float = 1) -> pd.Series:
    """
    Scale series so sum of absolute values equals a.
    
    Args:
        series: Input series
        a: Target sum of absolute values
    """
    abs_sum = np.abs(series).sum()
    if abs_sum == 0:
        return pd.Series(0, index=series.index)
    return series * (a / abs_sum)

@calc_by_symbol
def decay_linear(series: pd.Series, periods: int) -> pd.Series:
    """
    Calculate linearly decaying weighted average.
    
    Args:
        series: Input series
        periods: Decay window
    """
    weights = np.arange(1, periods + 1)[::-1]
    weights = weights / weights.sum()
    
    result = pd.Series(index=series.index)
    for i in range(periods-1, len(series)):
        result.iloc[i] = np.sum(series.iloc[i-periods+1:i+1] * weights)
    return result

# Additional functions from old codebase
@calc_by_symbol
def quantile(series: pd.Series, periods: int, q: float = 0.8) -> pd.Series:
    """Calculate rolling quantile."""
    return series.rolling(periods, min_periods=1).quantile(q)

@calc_by_symbol
def delay(series: pd.Series, periods: int = 5) -> pd.Series:
    """Alias for shift."""
    return shift(series, periods)

@calc_by_symbol
def mean(series: pd.Series, periods: int = 20) -> pd.Series:
    """Alias for ma."""
    return ma(series, periods)

@calc_by_symbol
def delta(series: pd.Series, periods: int = 20) -> pd.Series:
    """Calculate difference between current value and lagged value."""
    return series - shift(series, periods)

@calc_by_symbol
def ts_argmin(series: pd.Series, periods: int = 5) -> pd.Series:
    """Return position of rolling minimum."""
    return series.rolling(periods, min_periods=2).apply(lambda x: x.argmin())

@calc_by_symbol
def ts_argmax(series: pd.Series, periods: int = 5) -> pd.Series:
    """Return position of rolling maximum."""
    return series.rolling(periods, min_periods=2).apply(lambda x: x.argmax())

@calc_by_symbol
def product(series: pd.Series, periods: int) -> pd.Series:
    """Calculate rolling product."""
    return series.rolling(window=periods).apply(np.product)

@calc_by_symbol
def slope_pair(left: pd.Series, right: pd.Series, periods: int = 18) -> pd.Series:
    """
    Calculate slope between two series using linear regression.
    
    Args:
        left: Y series
        right: X series
        periods: Rolling window size
        
    Returns:
        Series of slopes
    """
    slopes = []
    for i in range(len(left)):
        if i < (periods - 1):
            slopes.append(np.nan)
        else:
            x = right[i - periods + 1:i + 1]
            y = left[i - periods + 1:i + 1]
            slope, _ = np.polyfit(x, y, 1)
            slopes.append(slope)
    
    return pd.Series(slopes, index=left.index)

@calc_by_symbol
def stddev(series: pd.Series, periods: int = 5) -> pd.Series:
    """Alias for std function."""
    return std(series, periods)
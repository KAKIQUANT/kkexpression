import numpy as np
import pandas as pd
from typing import Union, Optional, Tuple
from .utils import calc_by_symbol, calc_by_date, rolling_window
import talib
import logging

logger = logging.getLogger(__name__)

if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)

@calc_by_symbol
def correlation(left: pd.Series, right: pd.Series, periods: int = 20) -> pd.Series:
    """Calculate rolling correlation between two series."""
    left_num = pd.to_numeric(left, errors='coerce')
    right_num = pd.to_numeric(right, errors='coerce')
    
    # Calculate correlation for each window
    result = left_num.rolling(window=periods).corr(right_num)
    return result

@calc_by_symbol
def covariance(left: pd.Series, right: pd.Series, periods: int = 10) -> pd.Series:
    """Calculate rolling covariance between two series."""
    return left.rolling(window=periods).cov(right)

@calc_by_symbol
def ma(series: pd.Series, periods: int = 20) -> pd.Series:
    """Calculate simple moving average."""
    numeric_series = pd.to_numeric(series, errors='coerce')
    return numeric_series.rolling(window=periods).mean()

@calc_by_symbol
def std(series: pd.Series, periods: int = 20) -> pd.Series:
    """Calculate rolling standard deviation."""
    numeric_series = pd.to_numeric(series, errors='coerce')
    
    def calc_std(x):
        return x.rolling(window=periods).std()
    
    return numeric_series.groupby(level='symbol', group_keys=False).apply(calc_std)

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
    """
    Calculate rolling rank within time series.
    
    Args:
        series: Input time series
        periods: Rolling window size
        
    Returns:
        Rolling percentile rank (0-1) for each value
    """
    def rolling_rank(x):
        if len(x) < periods:
            return np.nan
        # Handle constant values in window
        if np.allclose(x.iloc[0], x.iloc[1:]):
            return 0.5
        # Calculate rank relative to window
        ranks = pd.Series(x).rank(pct=True)
        return ranks.iloc[-1]
    
    numeric_series = pd.to_numeric(series, errors='coerce')
    result = numeric_series.rolling(window=periods, min_periods=periods).apply(rolling_rank)
    result.name = f"{series.name}_{periods}"
    return result

@calc_by_symbol
def sum(series: pd.Series, periods: int) -> pd.Series:
    """Calculate rolling sum."""
    numeric_series = pd.to_numeric(series, errors='coerce')
    result = numeric_series.groupby(level='symbol', group_keys=False).apply(
        lambda x: x.rolling(window=periods).sum()
    )
    result.name = f'sum_{periods}'
    return result

@calc_by_symbol
def shift(se: pd.Series, N: int) -> pd.Series:
    """
    Shift series by N periods.
    
    Args:
        se: Input series
        N: Number of periods to shift
        
    Returns:
        Shifted series
    """
    try:
        numeric_series = pd.to_numeric(se, errors='coerce')
        return numeric_series.shift(N)
    except Exception as e:
        logger.error(f"Error in shift: {str(e)}")
        return pd.Series(np.nan, index=se.index)

@calc_by_symbol
def roc(se: pd.Series, N: int) -> pd.Series:
    """
    Calculate rate of change.
    
    Args:
        se: Input series
        N: Look-back periods
        
    Returns:
        Rate of change series
    """
    return se / shift(se, N) - 1

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
    series = pd.to_numeric(series, errors='coerce')
    abs_sum = np.abs(series).sum()
    if abs_sum == 0:
        raise ValueError("Cannot scale series with zero sum of absolute values")
    return series * (a / abs_sum)

@calc_by_symbol
def decay_linear(series: pd.Series, window: int) -> pd.Series:
    """Apply linear decay to time series."""
    weights = np.arange(1, window + 1)  # Linear weights
    weights = weights / weights.sum()
    
    def weighted_mean(x):
        if len(x) < window:
            return np.nan
        return np.sum(x * weights[-len(x):])
    
    return series.rolling(window=window, min_periods=window).apply(weighted_mean)

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
    """Calculate rolling mean."""
    numeric_series = pd.to_numeric(series, errors='coerce')
    return numeric_series.rolling(window=periods).mean()

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
def slope_pair(se_left: pd.Series, se_right: pd.Series, N: int = 18) -> pd.Series:
    """
    Calculate rolling slope between two series using linear regression.
    
    Args:
        se_left: Y series (dependent variable)
        se_right: X series (independent variable)
        N: Window size
        
    Returns:
        Series of rolling regression slopes
    """
    slopes = []
    R2 = []  # Keep R2 for potential future use
    
    for i in range(len(se_left)):
        if i < (N - 1):
            slopes.append(np.nan)
            R2.append(np.nan)
        else:
            x = se_right[i - N + 1:i + 1]
            y = se_left[i - N + 1:i + 1]
            try:
                slope, intercept = np.polyfit(x, y, 1)
                if np.isnan(slope):
                    slopes.append(np.nan)
                else:
                    slopes.append(slope)
            except:
                slopes.append(np.nan)
            
    slopes = pd.Series(slopes, index=se_left.index)
    return slopes

@calc_by_symbol
def stddev(series: pd.Series, periods: int = 5) -> pd.Series:
    """Alias for std function."""
    return std(series, periods)

@calc_by_symbol
def ts_corr(left: pd.Series, right: pd.Series, periods=20):
    """Calculate rolling correlation."""
    left_num = pd.to_numeric(left)
    right_num = pd.to_numeric(right)
    res = left_num.rolling(window=periods).corr(right_num)
    mask = (
        np.isclose(left_num.rolling(periods, min_periods=1).std(), 0, atol=2e-05) |
        np.isclose(right_num.rolling(periods, min_periods=1).std(), 0, atol=2e-05)
    )
    res[mask] = np.nan
    return res

@calc_by_symbol
def RSRS(high: pd.Series, low: pd.Series, N: int = 18):
    """Calculate RSRS indicator."""
    def numpy_rolling_regress(x1, y1, window: int = 18, array: bool = False):
        x_series = np.array(x1)
        y_series = np.array(y1)
        dd = x_series
        x = rolling_window(dd, window)
        yT = rolling_window(y_series, window)
        y = np.array([i.reshape(window, 1) for i in yT])
        ones_vector = np.ones((1, x.shape[1]))
        XT = np.stack([np.vstack([ones_vector, row]) for row in x])
        X = np.array([matrix.T for matrix in XT])
        reg_result = np.linalg.pinv(XT @ X) @ XT @ y
        return reg_result

    beta_series = numpy_rolling_regress(low, high, window=N, array=True)
    beta = beta_series.reshape(-1, 2)[:, 1]
    len_to_pad = len(low.index) - len(beta)
    pad = [np.nan for i in range(len_to_pad)]
    pad.extend(beta)
    beta = pd.Series(pad, index=low.index)
    return beta

@calc_by_symbol
def sign(series: pd.Series) -> pd.Series:
    """
    Return element-wise sign indication.
    
    Args:
        series: Input series
        
    Returns:
        Series with signs: -1 for negative, 0 for zero, 1 for positive
    """
    return np.sign(series)

@calc_by_symbol
def ta_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """Calculate On Balance Volume."""
    try:
        close = pd.to_numeric(close, errors='coerce')
        volume = pd.to_numeric(volume, errors='coerce')
        
        # Manual OBV calculation
        sign = np.where(close > close.shift(1), 1, 
                       np.where(close < close.shift(1), -1, 0))
        obv = (sign * volume).groupby(level='symbol').cumsum()
        return pd.Series(obv, index=close.index)
            
    except Exception as e:
        logger.error(f"Error calculating OBV: {str(e)}")
        return pd.Series(np.nan, index=close.index)

@calc_by_symbol
def scale(series: pd.Series, a: float = 1.0) -> pd.Series:
    """
    Scale series so sum of absolute values equals target value.
    
    Args:
        series: Input series
        a: Target sum of absolute values
        
    Returns:
        Scaled series
    """
    series = pd.to_numeric(series, errors='coerce')
    sum_abs = np.abs(series).sum()
    
    if sum_abs == 0:
        raise ValueError("Cannot scale series with zero sum of absolute values")
        
    scale_factor = a / sum_abs
    return series * scale_factor

@calc_by_symbol
def zscore(se: pd.Series, N: int) -> pd.Series:
    """
    Calculate rolling z-score.
    
    Args:
        se: Input series
        N: Window size
        
    Returns:
        Z-score series
    """
    def _zscore(x):
        try:
            x = x.dropna()
            value = (x[-1] - x.mean()) / x.std()
            return value if not np.isnan(value) else -1
        except:
            return -1

    ret = se.rolling(window=N).apply(lambda x: _zscore(x))
    return ret
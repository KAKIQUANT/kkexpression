import pandas as pd
import numpy as np
import talib
from typing import Tuple
from .utils import calc_by_symbol

@calc_by_symbol
def bbands_up(close: pd.Series, timeperiod: int = 20, 
              nbdevup: float = 2, nbdevdn: float = 2) -> pd.Series:
    """Calculate Bollinger Bands upper band."""
    try:
        upper, _, _ = talib.BBANDS(close, timeperiod=timeperiod,
                                 nbdevup=nbdevup, nbdevdn=nbdevdn)
        return pd.Series(upper, index=close.index)
    except Exception as e:
        return pd.Series(np.nan, index=close.index)

@calc_by_symbol
def bbands_down(close: pd.Series, timeperiod: int = 20,
                nbdevup: float = 2, nbdevdn: float = 2) -> pd.Series:
    """Calculate Bollinger Bands lower band."""
    try:
        _, _, lower = talib.BBANDS(close, timeperiod=timeperiod,
                                 nbdevup=nbdevup, nbdevdn=nbdevdn)
        return pd.Series(lower, index=close.index)
    except Exception as e:
        return pd.Series(np.nan, index=close.index)

@calc_by_symbol
def ta_atr(high: pd.Series, low: pd.Series, close: pd.Series,
           period: int = 14) -> pd.Series:
    """Calculate Average True Range."""
    try:
        atr = talib.ATR(high, low, close, period)
        return pd.Series(atr, index=high.index)
    except Exception as e:
        return pd.Series(np.nan, index=high.index)

@calc_by_symbol
def ta_obv(close: pd.Series, volume: pd.Series) -> pd.Series:
    """Calculate On Balance Volume."""
    try:
        obv = talib.OBV(close, volume)
        return pd.Series(obv, index=close.index)
    except Exception as e:
        return pd.Series(np.nan, index=close.index)

@calc_by_symbol
def rsi(series: pd.Series, periods: int = 14) -> pd.Series:
    """Calculate RSI."""
    delta = pd.to_numeric(series).diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=periods).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=periods).mean()
    rs = gain / loss
    return (100 - (100 / (1 + rs))).astype(str)

@calc_by_symbol
def max_(left: pd.Series, right: pd.Series) -> pd.Series:
    """Element-wise maximum."""
    left_num = pd.to_numeric(left, errors='coerce')
    right_num = pd.to_numeric(right, errors='coerce')
    return np.maximum(left_num, right_num)

@calc_by_symbol
def min_(left: pd.Series, right: pd.Series) -> pd.Series:
    """Element-wise minimum."""
    left_num = pd.to_numeric(left, errors='coerce')
    right_num = pd.to_numeric(right, errors='coerce')
    return np.minimum(left_num, right_num) 
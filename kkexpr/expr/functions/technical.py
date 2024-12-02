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
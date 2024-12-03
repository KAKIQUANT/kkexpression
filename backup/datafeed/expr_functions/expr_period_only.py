import math

import numpy as np
import pandas as pd
#import talib
import ta
from ta.volatility import BollingerBands

from .expr_utils import *


@calc_by_symbol
def ta_aroonosc(high, low, d):
    high.ffill(inplace=True)
    low.ffill(inplace=True)

    ret = talib.AROONOSC(high, low, d)
    return ret


@calc_by_symbol
def ta_ADX(high, low, close, d):
    high.ffill(inplace=True)
    low.ffill(inplace=True)
    close.ffill(inplace=True)
    ret = talib.ADX(high, low, close, d)
    return ret


@calc_by_symbol
def ta_atr(high, low, close, period=14):
    se = talib.ATR(high, low, close, period)
    # se = se / close.mean()
    se = pd.Series(se)
    se.index = high.index
    return se


@calc_by_symbol
def slope(close: pd.Series, d: int = 20):
    def _slope(close):
        y = np.log(close)
        x = np.arange(y.size)
        slope, intercept = np.polyfit(x, y, 1)
        annualized_returns = math.pow(math.exp(slope), 250) - 1
        r_squared = 1 - (sum((y - (slope * x + intercept)) ** 2) / ((len(y) - 1) * np.var(y, ddof=1)))
        score = annualized_returns * r_squared
        return score

    score = close.rolling(window=d).apply(lambda sub: _slope(sub))
    return score


@calc_by_symbol
def bbands_up(close, timeperiod=20, nbdevup=2, nbdevdn=2):
    # Initialize Bollinger Bands Indicator
    indicator_bb = BollingerBands(close, window=timeperiod, window_dev=nbdevup)

    upper_band = indicator_bb.bollinger_hband()
    #upper_band, middle_band, lower_band = talib.BBANDS(close, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn)
    return upper_band


@calc_by_symbol
def bbands_down(close, timeperiod=20, nbdevup=2, nbdevdn=2):
    # Add Bollinger Band low indicator
    indicator_bb = BollingerBands(close, window=timeperiod, window_dev=nbdevup)
    lower_band = indicator_bb.bollinger_lband()
    # upper_band, middle_band, lower_band = talib.BBANDS(close, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn)
    return lower_band

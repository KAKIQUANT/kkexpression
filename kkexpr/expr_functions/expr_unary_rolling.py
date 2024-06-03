import numpy as np
import pandas as pd
from .expr_utils import calc_by_symbol, calc_by_date


@calc_by_symbol
def delay(se: pd.Series, periods=5):
    return se.shift(periods=periods)


@calc_by_symbol
def delta(se: pd.Series, periods=20):
    se_result = se - se.shift(periods=periods)
    return se_result


@calc_by_symbol
def ts_min(se: pd.Series, periods=5):
    return se.rolling(window=periods).min()


@calc_by_symbol
def ts_max(se: pd.Series, periods=5):
    return se.rolling(window=periods).max()


@calc_by_symbol
def ts_argmin(se: pd.Series, periods=5):
    return se.rolling(periods, min_periods=2).apply(lambda x: x.argmin())


@calc_by_symbol
def ts_argmax(se: pd.Series, periods=5):
    return se.rolling(periods, min_periods=2).apply(lambda x: x.argmax())


@calc_by_symbol
def stddev(se, periods=5):
    return se.rolling(window=periods).std()


@calc_by_date
def rank(se: pd.Series):
    ret = se.rank(pct=True)
    return ret


@calc_by_symbol
def ts_rank(se: pd.Series, periods=9):
    ret = se.rolling(window=periods).rank(pct=True)
    return ret


@calc_by_symbol
def sum(se: pd.Series, N):
    ret = se.rolling(N).sum()
    ret.name = 'sum_{}'.format(N)
    return ret


@calc_by_symbol
def shift(se: pd.Series, N):
    return se.shift(N)


@calc_by_symbol
def roc(se: pd.Series, N):
    return se / shift(se, N) - 1


@calc_by_symbol
def product(se: pd.Series, d):
    return se.rolling(window=d).apply(np.product)


@calc_by_symbol
def zscore(se: pd.Series, N):
    def _zscore(x):

        try:
            x.dropna(inplace=True)
            print('sub', x)
            value = (x[-1] - x.mean()) / x.std()
            if value:
                return value
        except:
            return -1

    print(se)
    ret = se.rolling(window=N).apply(lambda x: _zscore(x))
    return ret

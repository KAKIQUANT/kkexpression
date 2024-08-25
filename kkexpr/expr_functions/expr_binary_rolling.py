import numpy as np
import pandas as pd
from .expr_utils import calc_by_symbol


@calc_by_symbol
def ts_corr(left: pd.Series, right: pd.Series, periods=20):
    res = left.rolling(window=periods).corr(right)
    # left.rolling(window=periods).apply(func=func,right)
    res.loc[
        np.isclose(left.rolling(periods, min_periods=1).std(), 0, atol=2e-05)
        | np.isclose(right.rolling(periods, min_periods=1).std(), 0, atol=2e-05)
        ] = np.nan
    return res


@calc_by_symbol
def ts_cov(left: pd.Series, right: pd.Series, periods=10):
    res = left.rolling(window=periods).cov(right)
    return res


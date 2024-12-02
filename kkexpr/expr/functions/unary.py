import numpy as np
import pandas as pd
from typing import Union
from .utils import calc_by_symbol, calc_by_date

@calc_by_symbol
def sign(series: pd.Series) -> pd.Series:
    """Return element-wise sign indication."""
    return np.sign(series)

@calc_by_date
def rank(series: pd.Series) -> pd.Series:
    """Return cross-sectional ranks."""
    return series.rank(pct=True)

@calc_by_symbol
def log(series: pd.Series) -> pd.Series:
    """Return natural logarithm."""
    return np.log(series)

@calc_by_symbol
def abs_(series: pd.Series) -> pd.Series:
    """Return absolute values."""
    return np.abs(series) 
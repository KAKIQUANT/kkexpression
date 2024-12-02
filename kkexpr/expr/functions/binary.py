import pandas as pd
import numpy as np
from typing import Union
from .utils import calc_by_symbol

@calc_by_symbol
def greater(left: pd.Series, right: pd.Series) -> pd.Series:
    """Return element-wise maximum."""
    return np.maximum(left, right)

@calc_by_symbol
def less(left: pd.Series, right: pd.Series) -> pd.Series:
    """Return element-wise minimum."""
    return np.minimum(left, right)

@calc_by_symbol
def cross_up(left: pd.Series, right: pd.Series) -> pd.Series:
    """Return True when left crosses above right."""
    diff = left - right
    diff_shift = diff.shift(1)
    return (diff >= 0) & (diff_shift < 0)

@calc_by_symbol
def cross_down(left: pd.Series, right: pd.Series) -> pd.Series:
    """Return True when left crosses below right."""
    diff = left - right
    diff_shift = diff.shift(1)
    return (diff <= 0) & (diff_shift > 0)

@calc_by_symbol
def calc_signal(long: pd.Series, exit: pd.Series) -> pd.Series:
    """Calculate trading signals."""
    long.name = 'signal_long'
    exit.name = 'signal_exit'
    df = pd.concat([long, exit], axis=1)
    df['signal'] = np.where(df['signal_long'], 1, np.nan)
    df['signal'] = np.where(df['signal_exit'], 0, df['signal'])
    df['signal'] = df['signal'].ffill()
    df['signal'] = df['signal'].fillna(0)
    return df['signal']

@calc_by_symbol
def gt(left: pd.Series, right: Union[pd.Series, float]) -> pd.Series:
    """Return True where left > right."""
    return left > right

@calc_by_symbol
def lt(left: pd.Series, right: Union[pd.Series, float]) -> pd.Series:
    """Return True where left < right."""
    return left < right

@calc_by_symbol
def ge(left: pd.Series, right: Union[pd.Series, float]) -> pd.Series:
    """Return True where left >= right."""
    return left >= right

@calc_by_symbol
def le(left: pd.Series, right: Union[pd.Series, float]) -> pd.Series:
    """Return True where left <= right."""
    return left <= right

@calc_by_symbol
def eq(left: pd.Series, right: Union[pd.Series, float]) -> pd.Series:
    """Return True where left == right."""
    return left == right

@calc_by_symbol
def ne(left: pd.Series, right: Union[pd.Series, float]) -> pd.Series:
    """Return True where left != right."""
    return left != right

@calc_by_symbol
def and_(left: pd.Series, right: pd.Series) -> pd.Series:
    """Logical AND of two boolean series."""
    return left & right

@calc_by_symbol
def or_(left: pd.Series, right: pd.Series) -> pd.Series:
    """Logical OR of two boolean series."""
    return left | right

@calc_by_symbol
def xor(left: pd.Series, right: pd.Series) -> pd.Series:
    """Logical XOR of two boolean series."""
    return left ^ right

@calc_by_symbol
def max_(left: pd.Series, right: Union[pd.Series, float]) -> pd.Series:
    """Element-wise maximum."""
    return np.maximum(left, right)

@calc_by_symbol
def min_(left: pd.Series, right: Union[pd.Series, float]) -> pd.Series:
    """Element-wise minimum."""
    return np.minimum(left, right)

@calc_by_symbol
def where(cond: pd.Series, left: pd.Series, right: pd.Series) -> pd.Series:
    """
    Return elements from left where cond is True, otherwise from right.
    
    Args:
        cond: Boolean condition
        left: Values to use where condition is True
        right: Values to use where condition is False
        
    Returns:
        Series with values selected based on condition
    """
    return pd.Series(np.where(cond, left, right), index=cond.index)

# ... (rest of binary functions) 
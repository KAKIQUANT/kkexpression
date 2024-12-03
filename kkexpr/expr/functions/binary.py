import pandas as pd
import numpy as np
from typing import Union
from .utils import calc_by_symbol

@calc_by_symbol
def greater(left: pd.Series, right: pd.Series) -> pd.Series:
    """Return element-wise maximum."""
    return (left > right).astype(bool)

@calc_by_symbol
def less(left: pd.Series, right: pd.Series) -> pd.Series:
    """Return element-wise minimum."""
    return (left < right).astype(bool)

@calc_by_symbol
def cross_up(left: pd.Series, right: pd.Series) -> pd.Series:
    """
    Return True when left crosses above right.
    
    A cross up occurs when:
    1. Current value of left is greater than current value of right
    2. Previous value of left was less than or equal to previous value of right
    """
    # Convert to numeric
    left = pd.to_numeric(left, errors='coerce')
    right = pd.to_numeric(right, errors='coerce')
    
    # Calculate current and previous conditions
    curr_diff = left - right
    prev_diff = curr_diff.shift(1)
    
    # Cross up occurs when current diff is positive and previous diff was negative
    return (curr_diff > 0) & (prev_diff <= 0)

@calc_by_symbol
def cross_down(left: pd.Series, right: pd.Series) -> pd.Series:
    """
    Return True when left crosses below right.
    
    A cross down occurs when:
    1. Current value of left is less than current value of right
    2. Previous value of left was greater than or equal to previous value of right
    """
    # Convert to numeric
    left = pd.to_numeric(left, errors='coerce')
    right = pd.to_numeric(right, errors='coerce')
    
    # Calculate current and previous conditions
    curr_diff = left - right
    prev_diff = curr_diff.shift(1)
    
    # Cross down occurs when current diff is negative and previous diff was positive
    return (curr_diff < 0) & (prev_diff >= 0)

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
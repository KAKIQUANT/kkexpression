from typing import Callable, Dict
import numpy as np
import pandas as pd

class Operator:
    """Base class for custom operators."""
    
    # Class-level registry
    registry: Dict[str, 'Operator'] = {}
    
    def __init__(self, func: Callable):
        self.func = func
        
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)

def register_operator(name: str, func: Callable) -> None:
    """Register a new operator."""
    op = Operator(func)
    Operator.registry[name] = op
    # We'll register with Factor class later to avoid circular import
    
# Import functions after Operator class definition
from kkexpr.expr.functions import (
    greater, less, cross_up, cross_down,
    correlation, covariance, ma, std, ts_max, ts_min,
    ts_rank, sum, shift, roc, zscore,
    bbands_up, bbands_down, ta_atr, ta_obv, rsi,
    sign, rank, log, abs_
)

# Register operators
register_operator('MA', ma)
register_operator('SMA', ma)
register_operator('EMA', lambda x, n: x.ewm(span=n).mean())
register_operator('STD', std)
register_operator('MIN', less)
register_operator('MAX', greater)
register_operator('REF', shift)
register_operator('DELAY', shift)
register_operator('RANK', ts_rank)
register_operator('SUM', sum)
register_operator('ROC', roc)
register_operator('ZSCORE', zscore)
register_operator('CORR', correlation)
register_operator('COV', covariance)
register_operator('CROSS_UP', cross_up)
register_operator('CROSS_DOWN', cross_down)
register_operator('SIGN', sign)
register_operator('LOG', log)
register_operator('ABS', abs_)

# Technical indicators
register_operator('RSI', rsi)
register_operator('ATR', ta_atr)
register_operator('OBV', ta_obv)
register_operator('BBANDS_UP', bbands_up)
register_operator('BBANDS_DOWN', bbands_down) 
from functools import wraps
import pandas as pd
from typing import Callable, Any
import logging
from numpy.lib.stride_tricks import as_strided as strided
import numpy as np

logger = logging.getLogger(__name__)

def calc_by_symbol(func):
    """Decorator to apply function by symbol group."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        other_args = []
        se_args = []
        se_names = []
        
        for i, arg in enumerate(args):
            if not isinstance(arg, pd.Series):
                other_args.append(arg)
            else:
                se_args.append(arg)
                if arg.name:
                    se_names.append(arg.name)
                else:
                    name = f'arg_{i}'
                    arg.name = name
                    se_names.append(name)
                    
        if len(se_args) == 1:
            ret = se_args[0].groupby(level=0, group_keys=False).apply(
                lambda x: func(x, *other_args, **kwargs)
            )
            ret.name = f"{func.__name__}_{se_names[0]}"
            if other_args:
                ret.name += f"_{other_args[0]}"
        elif len(se_args) > 1:
            df = pd.concat(se_args, axis=1)
            df.columns = se_names
            
            if len(df.index.get_level_values(0).unique()) == 1:
                ret = func(*[df[name] for name in se_names], *other_args)
            else:
                ret = df.groupby(level=0, group_keys=False).apply(
                    lambda x: func(*[x[name] for name in se_names], *other_args)
                )
        else:
            logger.error(f"No Series arguments provided to {func.__name__}")
            return None
            
        return ret
    return wrapper

def calc_by_date(func: Callable) -> Callable:
    """Decorator to apply function by date."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> pd.Series:
        try:
            # Extract series and other arguments
            series_args = [arg for arg in args if isinstance(arg, pd.Series)]
            other_args = [arg for arg in args if not isinstance(arg, pd.Series)]
            
            if not series_args:
                raise ValueError("No Series arguments provided")
                
            # Group by date and apply function
            result = series_args[0].groupby(level=0).apply(
                lambda x: func(x, *other_args, **kwargs)
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            return pd.Series(index=args[0].index)
            
    return wrapper 

def rolling_window(a: np.array, window: int) -> np.array:
    """
    Create a rolling window view of the input array.
    
    Args:
        a: Input array
        window: Size of the rolling window
        
    Returns:
        Array of rolling windows
    """
    shape = a.shape[:-1] + (a.shape[-1] - window + 1, window)
    strides = a.strides + (a.strides[-1],)
    return strided(a, shape=shape, strides=strides)

@calc_by_date
def rank(series: pd.Series) -> pd.Series:
    """Calculate cross-sectional rank."""
    def rank_by_date(x):
        return x.rank(pct=True)
    
    if isinstance(series.index, pd.MultiIndex):
        # Group by date and calculate rank
        result = series.groupby(level=1, group_keys=False).transform(rank_by_date)
        return pd.Series(result, index=series.index, name=series.name)
    
    return rank_by_date(series)
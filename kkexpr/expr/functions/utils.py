from functools import wraps
import pandas as pd
from typing import Callable, Any
import logging

logger = logging.getLogger(__name__)

def calc_by_symbol(func: Callable) -> Callable:
    """Decorator to apply function by symbol."""
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> pd.Series:
        try:
            # Extract series and other arguments
            series_args = [arg for arg in args if isinstance(arg, pd.Series)]
            other_args = [arg for arg in args if not isinstance(arg, pd.Series)]
            
            if not series_args:
                raise ValueError("No Series arguments provided")
                
            # Group by symbol and apply function
            result = series_args[0].groupby(level=1).apply(
                lambda x: func(x, *other_args, **kwargs)
            )
            
            return result
            
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            return pd.Series(index=args[0].index)
            
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
import pandas as pd
import numpy as np
from typing import Optional

def winsorize(data: pd.DataFrame, method: str = 'mad', n_std: float = 3) -> pd.DataFrame:
    """Winsorize factor data."""
    if method == 'mad':
        median = data.median()
        mad = (data - median).abs().median()
        upper = median + n_std * mad
        lower = median - n_std * mad
    elif method == 'std':
        mean = data.mean()
        std = data.std()
        upper = mean + n_std * std
        lower = mean - n_std * std
        
    return data.clip(lower=lower, upper=upper)

def standardize(data: pd.DataFrame) -> pd.DataFrame:
    """Standardize factor data."""
    return (data - data.mean()) / data.std()

def neutralize(data: pd.DataFrame,
              groups: pd.DataFrame,
              style_factors: Optional[pd.DataFrame] = None) -> pd.DataFrame:
    """Neutralize factor data by groups and style factors."""
    # Group neutralization
    group_means = data.groupby(groups).transform('mean')
    data = data - group_means
    
    # Style factor neutralization
    if style_factors is not None:
        from sklearn.linear_model import LinearRegression
        reg = LinearRegression()
        reg.fit(style_factors, data)
        data = data - reg.predict(style_factors)
        
    return data 
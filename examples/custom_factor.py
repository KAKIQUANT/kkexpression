"""
Custom factor example showing how to:
1. Create custom operators
2. Create custom base factors
3. Use them in factor calculations
"""

import pandas as pd
import numpy as np
from kkexpr import Factor
from kkexpr.extension import (
    RollingWindowFactor,
    UserDefinedLeafFactor
)

def custom_volatility(series: np.ndarray, window: int) -> np.ndarray:
    """Calculate custom volatility measure."""
    return np.sqrt(np.sum(np.square(np.diff(series[-window:]))))

def MY_VOL(factor: Factor, window: int) -> Factor:
    """Custom volatility operator."""
    return RollingWindowFactor(custom_volatility, window, factor)

def get_minute_prices(order_book_ids: list, start_date: str, end_date: str) -> pd.DataFrame:
    """Get 1-minute price data and calculate intraday volatility."""
    # Implementation depends on your data source
    pass

def main():
    # Create custom base factor
    intraday_vol = UserDefinedLeafFactor(
        'intraday_vol',
        get_minute_prices
    )
    
    # Create factor using custom operator
    close = Factor('close')
    vol_factor = MY_VOL(close, 20)
    
    # Combine custom factors
    combined_factor = vol_factor * intraday_vol
    
    # Execute calculation
    symbols = ['000001.SH', '000300.SH']
    start_date = '20230101'
    end_date = '20231231'
    
    result = combined_factor.execute(
        order_book_ids=symbols,
        start_date=start_date,
        end_date=end_date
    )
    
    print("Custom factor result:")
    print(result.head())

if __name__ == '__main__':
    main() 
import sys
from pathlib import Path
sys.path.append('../')

import pandas as pd
import numpy as np
from kkexpr.core import Factor
from kkexpr.data.loader import CSVDataloader

def main():
    # Initialize data loader for GOLD
    data_path = Path(__file__).parent.parent / 'kkexpr' / 'data' / 'quotes'
    loader = CSVDataloader(
        path=data_path,
        symbols=['GOLD'],
        start_date='20230101',
        end_date='20240331'
    )
    
    # Load base data and convert to numeric
    df = loader.load()
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col])
    
    print("\n1. Data Sample:")
    print(df.head())
    
    # Calculate returns
    df['returns'] = df['close'].groupby(level='symbol').shift(1)
    df['returns'] = df['close'] / df['returns'] - 1
    
    # Create WorldQuant101 Alpha1 factor
    alpha1_expr = '((ts_rank(volume, 32) * (1 - ts_rank(((close + high) - low), 16))) * (1 - ts_rank(returns, 32)))'
    print("\n2. Alpha1 Expression:")
    print(alpha1_expr)
    
    # Test each component separately
    print("\n3. Testing Components:")
    
    # Component 1: Volume rank
    vol_rank = Factor("ts_rank(volume, 32)")
    vol_result = vol_rank.execute(
        order_book_ids=['GOLD'],
        frequency='1d',
        start_date='20230101',
        end_date='20240331',
        test_data=df
    )
    print("\nVolume Rank (first 5 non-null):")
    print(vol_result[vol_result.notna()].head())
    
    # Component 2: Price spread rank
    spread_rank = Factor("ts_rank(((close + high) - low), 16)")
    spread_result = spread_rank.execute(
        order_book_ids=['GOLD'],
        frequency='1d',
        start_date='20230101',
        end_date='20240331',
        test_data=df
    )
    print("\nPrice Spread Rank (first 5 non-null):")
    print(spread_result[spread_result.notna()].head())
    
    # Component 3: Returns rank
    ret_rank = Factor("ts_rank(returns, 32)")
    ret_result = ret_rank.execute(
        order_book_ids=['GOLD'],
        frequency='1d',
        start_date='20230101',
        end_date='20240331',
        test_data=df
    )
    print("\nReturns Rank (first 5 non-null):")
    print(ret_result[ret_result.notna()].head())
    
    # Full Alpha1 factor
    alpha1_factor = Factor(alpha1_expr)
    alpha1_result = alpha1_factor.execute(
        order_book_ids=['GOLD'],
        frequency='1d',
        start_date='20230101',
        end_date='20240331',
        test_data=df
    )
    
    print("\n4. Final Alpha1 Result:")
    print("\nFirst 5 non-null values:")
    print(alpha1_result[alpha1_result.notna()].head())
    
    print("\nBasic statistics:")
    valid_results = alpha1_result[alpha1_result.notna()]
    print(valid_results.describe())

if __name__ == "__main__":
    main() 
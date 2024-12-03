import sys
from pathlib import Path
sys.path.append('../')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from kkexpr.core import Factor
from kkexpr.data.loader import CSVDataloader
from kkexpr.factor import WorldQuant101

def test_single_factor(df: pd.DataFrame, name: str, field: str) -> pd.Series:
    """Test a single factor and return its results."""
    print(f"\nTesting {name}:")
    print(f"Expression: {field}")
    
    factor = Factor(field)
    result = factor.execute(
        order_book_ids=['GOLD'],
        frequency='1d',
        start_date='20230101',
        end_date='20240331',
        test_data=df
    )
    
    valid_results = result[result.notna()]
    print("\nBasic statistics:")
    print(valid_results.describe())
    
    return valid_results

def plot_factor_results(results: dict, title: str):
    """Plot factor results for comparison."""
    plt.figure(figsize=(15, 8))
    
    for name, values in results.items():
        # Normalize values for comparison
        normalized = (values - values.mean()) / values.std()
        normalized.plot(label=name, alpha=0.7)
    
    plt.title(title)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{title.lower().replace(" ", "_")}.png')
    plt.close()

def main():
    # Initialize data loader
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
    
    # Calculate returns
    df['returns'] = df['close'].groupby(level='symbol').shift(1)
    df['returns'] = df['close'] / df['returns'] - 1
    
    # Get WorldQuant101 factors
    wq101 = WorldQuant101()
    names, fields = wq101.get_fields_names()
    
    print(f"\nTesting {len(names)} WorldQuant101 Factors")
    
    # Test factors in groups
    results = {}
    
    # Volume-based factors (1, 2, 3, 6)
    volume_factors = [0, 1, 2, 5]  # indices of volume-related factors
    volume_results = {}
    for idx in volume_factors:
        result = test_single_factor(df, names[idx], fields[idx])
        volume_results[names[idx]] = result
    plot_factor_results(volume_results, "Volume-Based Factors")
    
    # Price-based factors (4, 5, 9, 10)
    price_factors = [3, 4, 8, 9]  # indices of price-related factors
    price_results = {}
    for idx in price_factors:
        result = test_single_factor(df, names[idx], fields[idx])
        price_results[names[idx]] = result
    plot_factor_results(price_results, "Price-Based Factors")
    
    # Momentum factors (7, 8)
    momentum_factors = [6, 7]  # indices of momentum-related factors
    momentum_results = {}
    for idx in momentum_factors:
        result = test_single_factor(df, names[idx], fields[idx])
        momentum_results[names[idx]] = result
    plot_factor_results(momentum_results, "Momentum-Based Factors")
    
    # Calculate correlations
    all_results = pd.DataFrame(results)
    print("\nFactor Correlations:")
    print(all_results.corr())

if __name__ == "__main__":
    main() 
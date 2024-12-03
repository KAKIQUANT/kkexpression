import sys
from pathlib import Path
sys.path.append('../')

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from kkexpr.core import Factor
from kkexpr.data.loader import CSVDataloader
from kkexpr.factor import (
    WorldQuant101, AlphaMomentum, AlphaVolatility, 
    AlphaValue, AlphaTechnical
)

def test_factor_group(df: pd.DataFrame, alpha_class, title: str) -> pd.DataFrame:
    """Test a group of factors from an alpha class."""
    print(f"\nTesting {title}")
    
    alpha = alpha_class()
    names, fields = alpha.get_fields_names()
    results = {}
    
    for name, field in zip(names, fields):
        print(f"\nCalculating {name}:")
        print(f"Expression: {field}")
        
        factor = Factor(field)
        result = factor.execute(
            order_book_ids=['GOLD'],
            frequency='1d',
            start_date='20230101',
            end_date='20240331',
            test_data=df
        )
        
        valid_result = result[result.notna()]
        results[name] = valid_result
        
        print("\nBasic statistics:")
        print(valid_result.describe())
    
    # Plot factor results
    plt.figure(figsize=(15, 8))
    for name, values in results.items():
        normalized = (values - values.mean()) / values.std()
        normalized.plot(label=name, alpha=0.7)
    
    plt.title(f"{title} Factors")
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f'{title.lower().replace(" ", "_")}_factors.png')
    plt.close()
    
    return pd.DataFrame(results)

def plot_correlation_matrix(results_df: pd.DataFrame, title: str):
    """Plot correlation matrix for factors."""
    plt.figure(figsize=(12, 10))
    sns.heatmap(
        results_df.corr(), 
        annot=True, 
        cmap='RdYlBu', 
        center=0,
        fmt='.2f'
    )
    plt.title(f"{title} Factor Correlations")
    plt.tight_layout()
    plt.savefig(f'{title.lower().replace(" ", "_")}_correlations.png')
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
    
    # Load and prepare data
    df = loader.load()
    for col in ['open', 'high', 'low', 'close', 'volume']:
        df[col] = pd.to_numeric(df[col])
    
    df['returns'] = df['close'].groupby(level='symbol').shift(1)
    df['returns'] = df['close'] / df['returns'] - 1
    
    # Test each factor group
    factor_groups = [
        (WorldQuant101, "WorldQuant101"),
        (AlphaMomentum, "Momentum"),
        (AlphaVolatility, "Volatility"),
        (AlphaValue, "Value"),
        (AlphaTechnical, "Technical")
    ]
    
    all_results = {}
    for alpha_class, title in factor_groups:
        results = test_factor_group(df, alpha_class, title)
        all_results[title] = results
        plot_correlation_matrix(results, title)
    
    # Calculate cross-group correlations
    cross_group = pd.concat([df.iloc[:,0] for df in all_results.values()], axis=1)
    plot_correlation_matrix(cross_group, "Cross Group")
    
    # Print summary statistics
    print("\nSummary Statistics:")
    for title, results in all_results.items():
        print(f"\n{title} Factors:")
        print(f"Number of factors: {results.shape[1]}")
        print(f"Average correlation: {results.corr().mean().mean():.3f}")
        print(f"Data coverage: {(results.notna().sum() / len(results) * 100).mean():.1f}%")

if __name__ == "__main__":
    main() 
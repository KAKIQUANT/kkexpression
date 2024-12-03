"""
Industry neutralization example showing how to:
1. Create industry neutral factors
2. Handle industry grouping
3. Analyze neutralized factors
"""

import pandas as pd
from kkexpr import Factor
from kkexpr.core.industry import industry_neutralize

def main():
    # Create base factor
    pe = Factor('pe_ratio')
    pb = Factor('pb_ratio')
    factor = 1/pe + 1/pb
    
    # Add preprocessing steps
    factor.winsorize(method='std', n_std=3)  # Like RQFactor
    factor.standardize()
    
    # Execute factor calculation
    symbols = ['000001.SH', '000300.SH']
    start_date = '20230101'
    end_date = '20231231'
    
    factor_data = factor.execute(
        order_book_ids=symbols,
        start_date=start_date,
        end_date=end_date
    )
    
    # Get industry data
    # This is placeholder - actual implementation depends on your data source
    industry_data = pd.DataFrame(index=factor_data.index)
    industry_data['industry'] = 'industry_code'
    
    # Neutralize factor
    neutral_factor = industry_neutralize(factor_data, industry_data)
    
    print("Original factor:")
    print(factor_data.head())
    print("\nNeutralized factor:")
    print(neutral_factor.head())

if __name__ == '__main__':
    main() 
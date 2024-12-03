"""
Alpha factor example showing how to:
1. Create alpha factors like RQFactor
2. Use cross-sectional operations
3. Handle factor preprocessing
"""

from kkexpr import Factor
from kkexpr.core.cross_section import cs_rank, cs_zscore, cs_demean

def create_momentum_factor():
    """Create a momentum factor similar to RQFactor style."""
    # Price momentum
    close = Factor('close')
    returns = close.pct_change()
    
    # Volume factor
    volume = Factor('volume')
    vol_ma = Factor('MA(volume, 20)')
    vol_factor = volume / vol_ma
    
    # Combine factors with cross-sectional operations
    mom_factor = cs_rank(returns) * cs_zscore(vol_factor)
    
    # Add preprocessing pipeline
    mom_factor.winsorize(method='mad', n_std=3)
    mom_factor.standardize()
    mom_factor.neutralize(groups='industry')
    
    return mom_factor

def create_value_factor():
    """Create a value factor similar to RQFactor style."""
    # Basic value metrics
    pb = Factor('pb_ratio')
    pe = Factor('pe_ratio')
    
    # Create composite value factor
    value_factor = cs_rank(1/pb) + cs_rank(1/pe)
    value_factor = cs_demean(value_factor)
    
    # Add preprocessing
    value_factor.winsorize()
    value_factor.standardize()
    
    return value_factor

def main():
    # Create factors
    mom = create_momentum_factor()
    value = create_value_factor()
    
    # Combine factors
    combined = 0.5 * mom + 0.5 * value
    
    # Execute calculation
    symbols = ['000001.SH', '000300.SH']
    start_date = '20230101'
    end_date = '20231231'
    
    result = combined.execute(
        order_book_ids=symbols,
        start_date=start_date,
        end_date=end_date
    )
    
    print("Combined factor result:")
    print(result.head())

if __name__ == '__main__':
    main() 